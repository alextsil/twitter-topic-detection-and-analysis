// Run within mongo shell using open("absolute path to this file")
var ops = [];
var cursor = db.tweets.find();

cursor.forEach(function (doc) {
    ops.push({
        "updateOne": {
            "filter": {"_id": doc._id},
            "update": {"$set": {"timestamp": new Date("doc.created_at")}}
        }
    });

    if (ops.length === 1000) {
        db.tweets.bulkWrite(ops);
        ops = [];
    }
});

if (ops.length > 0) db.tweets.bulkWrite(ops);