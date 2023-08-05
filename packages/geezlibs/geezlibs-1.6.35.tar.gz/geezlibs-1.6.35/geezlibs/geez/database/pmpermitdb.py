from geezlibs.geez.database import db_x

db_y = db_x["PMPERMIT"]

PMPERMIT_MESSAGE = (
    "**peringatan! tolong baca pesan ini dengan hati-hati..\n\n**"
    "**Saya Geez-Pyro Assistant untuk melindungi tuan saya dari spam**"
    "**jika Anda bukan spammer, harap tunggu!.\n\n**"
    "**jangan spam atau Anda akan diblokir!**"
)

BLOCKED = "**Spammer, blocked!**"

LIMIT = 5


async def set_pm(value: bool):
    doc = {"_id": 1, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await db_y.find_one({"_id": 1})
    r2 = await db_y.find_one({"_id": "Approved"})
    if r:
        await db_y.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await db_y.insert_one(doc)
    if not r2:
        await db_y.insert_one(doc2)


async def set_permit_message(text):
    await db_y.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


async def set_block_message(text):
    await db_y.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await db_y.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await db_y.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def approve_user(user_id):
    cd = await db_y.find_one({"_id": "PmPermit"})
    if cd:
        await db_y.update_one({"_id": "PmPermit"}, {"$push": {"user_id": user_id}})
    else:
        user_idc = [user_id]
        await db_y.insert_one({"_id": "PmPermit", "user_id": user_idc})


async def disapprove_user(user_id):
    await db_y.update_one({"_id": "PmPermit"}, {"$pull": {"user_id": user_id}})


async def is_user_approved(user_id):
    sm = await db_y.find_one({"_id": "PmPermit"})
    if sm:
        kek = list(sm.get("user_id"))
        return user_id in kek
    else:
        return False


async def user_list():
    sm = await db_y.find_one({"_id": "PmPermit"})
    if sm:
        return list(sm.get("user_id"))
    else:
        return False
