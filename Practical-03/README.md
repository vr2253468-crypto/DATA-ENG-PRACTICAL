# Practical 03 - MongoDB Operations Evidence

## Objective
Document basic MongoDB document operations: insert one, find, insert many, and formatted query output.

## Contents
- `Practical_3_MongoDB.docx`
- `step1_insertOne.png.png`
- `step2_find.png.png`
- `step3_insertMany.png.png`
- `step4_find_pretty.png.png`

## Prerequisites
- MongoDB shell (`mongosh`) if reproducing manually
- A MongoDB instance (local or hosted)

## Dependency notes
No executable `.js` script is present in this folder. This practical is documented using DOCX and screenshots.

## Reproduction commands (manual)
If reproducing the documented operations:

```javascript
use practical3
db.items.insertOne({ name: "laptop", price: 999 })
db.items.find()
db.products.insertMany([
  { name: "phone", price: 500, stock: 10 },
  { name: "tablet", price: 300, stock: 5 },
  { name: "watch", price: 150, stock: 0 }
])
db.products.find().pretty()
```

## Expected/available outputs
- Screenshots show successful command execution and query outputs.

## Troubleshooting
- If `mongosh` is unavailable, install MongoDB shell from official MongoDB docs.
- Ensure you are connected to a writable database.

## Verification status
- MongoDB commands were **not re-executed in this documentation stage**.

## Learning outcomes
- Distinguish single-document vs multi-document inserts.
- Retrieve and format MongoDB documents for inspection.
