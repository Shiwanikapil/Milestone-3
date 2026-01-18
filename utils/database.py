# utils/database.py
import os
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
import bcrypt 

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["ai_project_db"]

users = db.users
books = db.books
summaries = db.summaries

def oid(x):
    return ObjectId(str(x))

# ---------- USER ----------
def create_user(name, email, password):
    pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users.insert_one({
        "name": name,
        "email": email,
        "password": pwd,
       # "role": role,
        "is active": True,
        "created_at": datetime.utcnow()                                 
     })

def get_user_by_email(email):
    return users.find_one({"email": email})

def verify_user(email, password):
    u = get_user_by_email(email)
    if not u:
        return None
    if bcrypt.checkpw(password.encode(), u["password"]):
        return u
    return None

# ---------- BOOK ----------
def create_book(user_id, title,author, text):
    return books.insert_one({
        "user_id": oid(user_id),
        "title": title,
        "author": author,  
        "text": text,
        "created_at": datetime.utcnow()
    }).inserted_id

def update_book_status(book_id, status):
    books.update_one(
        {"_id": oid(book_id)},
        {"$set": {"status": status}}
    )


def get_books(user_id):
    return list(books.find(
        {"user_id": oid(user_id)}
    ).sort("created_at", DESCENDING))

def delete_book(book_id, user_id):
    summaries.delete_many({
        "book_id": oid(book_id),
        "user_id": oid(user_id)
    })

    books.delete_one({
        "_id": oid(book_id),
        "user_id": oid(user_id)
    })



def save_summary(book_id, user_id, summary_text, summary_type="default"):
    return summaries.insert_one({
        "book_id": oid(book_id),
        "user_id": oid(user_id),
        "summary_text": summary_text,
        "summary_type": summary_type,
        "is_favorite": False,
        "is_default": False,
        "created_at": datetime.utcnow()
    }).inserted_id


def get_all_summaries(book_id):
    return list(
        summaries.find({"book_id": oid(book_id)})
        .sort([
            ("is_favorite", -1),
            ("created_at", -1)
        ])
    )


def delete_summary(summary_id):
    summaries.delete_one(
        {"_id": oid(summary_id)}
    )


# ⭐ MARK FAVORITE SUMMARY
def set_favorite_summary(summary_id, book_id):
    # sab summaries ko unfavorite
    summaries.update_many(
        {"book_id": oid(book_id)},
        {"$set": {"is_favorite": False}}
    )

    # selected summary ko favorite
    summaries.update_one(
        {"_id": oid(summary_id)},
        {"$set": {"is_favorite": True}}
    )


# 🏷️ SET DEFAULT SUMMARY
def set_default_summary(summary_id, book_id):
    # sab summaries ko non-default
    summaries.update_many(
        {"book_id": oid(book_id)},
        {"$set": {"is_default": False}}
    )

    # selected summary ko default
    summaries.update_one(
        {"_id": oid(summary_id)},
        {"$set": {"is_default": True}}
    )
# ---------- SEARCH ----------
def search_books(user_id, title=None, status=None):
    q = {"user_id": oid(user_id)}

    if title:
        q["title"] = {"$regex": title, "$options": "i"}

    if status:
        q["status"] = status   # uploaded / summarized

    return list(books.find(q)) 

# ---------- ADMIN ANALYTICS ----------

def count_users():
    return users.count_documents({})

def count_books():
    return books.count_documents({})

def count_summaries():
    return summaries.count_documents({})

def get_all_users():
    return list(users.find({}, {"password_hash": 0}))

def get_all_books():
    return list(books.find()) 

#def get_all_summaries():
    #return list(summaries.find())

def get_user_book_count(user_id):
     return books.count_documents({"user_id": oid(user_id)})


# ---------- ADMIN HELPERS ----------

def get_all_users():
    return list(users.find().sort("created_at",-1))

def deactivate_user(user_id):
    users.update_one(
        {"_id": oid(user_id)},
        {"$set": {"is_active": False}}
    )

def activate_user(user_id):
    users.update_one(
        {"_id": oid(user_id)},
        {"$set": {"is_active": True}}
    )

def delete_user(user_id):
    users.delete_one({"_id": oid(user_id)})
    books.delete_many({"user_id": oid(user_id)})
    summaries.delete_many({"user_id": oid(user_id)}) 

def toggle_user_status(user_id):
    user = users.find_one({"_id": user_id})
    new_status = not user.get("active", True)

    users.update_one(
        {"_id": user_id},
        {"$set": {"active": new_status}}
    ) 


# ---------- ADMIN : USERS WITH THEIR BOOKS ----------
def get_users_with_books():
    pipeline = [
        {
            "$lookup": {
                "from": "books",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "books"
            }
        },
        {
            "$project": {
                "name": 1,
                "email": 1,
                "books": {
                    "$map": {
                        "input": "$books",
                        "as": "b",
                        "in": {
                            "_id": "$$b._id",
                            "title": "$$b.title",
                            "author": "$$b.author",
                            "created_at": "$$b.created_at"
                        }
                    }
                }
            }
        }
    ]
    return list(users.aggregate(pipeline))
# ---------- ADMIN : DELETE BOOK ----------
def admin_delete_book(book_id):
    books.delete_one(
        {"_id": ObjectId(book_id)}
    )
    summaries.delete_many(
        {"book_id": ObjectId(book_id)}
    )

# ---------- ADMIN : GET LATEST SUMMARY ----------
def admin_get_latest_summary(book_id):
    return summaries.find_one(
        {"book_id": ObjectId(book_id)},
        sort=[("created_at", -1)]
    ) 


def get_total_users():
    return users.count_documents({})

def get_active_users():
    return users.count_documents({})

def get_total_books():
    return books.count_documents({})

def get_total_summaries():
    return summaries.count_documents({})

def get_books_per_day():
    pipeline = [
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    result = books.aggregate(pipeline)
    return {r["_id"]: r["count"] for r in result}

def get_most_active_users(limit=5):
    pipeline = [
        {"$group": {"_id": "$user_id", "book_count": {"$sum": 1}}},
        {"$sort": {"book_count": -1}},
        {"$limit": limit}
    ]
    data = books.aggregate(pipeline)

    output = []
    for d in data:
        user = users.find_one({"_id": d["_id"]})
        if user:
            output.append({
                "name": user["name"],
                "book_count": d["book_count"]
            })
    return output


def get_user_dashboard_stats(user_id):
    user_oid = ObjectId(user_id)

    books_count = books.count_documents({
        "user_id": user_oid
    })

    summaries_count = summaries.count_documents({
        "user_id": user_oid,
        "summary_text": {"$exists": True, "$ne": ""}
    })

    recent_books = list(
        books.find({"user_id": user_oid})
        .sort("created_at", -1)
        .limit(5)
    )

    return {
        "books_count": books_count,
        "summaries_count": summaries_count,
        "recent_books": recent_books
    }
