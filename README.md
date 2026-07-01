# flask-ec2
you can test the CRUD endpoints from your browser's address bar or terminal:
# Create a task
curl -X POST http://3.236.198.195:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My first AWS task"}'

# Read all tasks
curl http://3.236.198.195:5000/tasks

# Update task (replace 1 with actual id)
curl -X PUT http://3.236.198.195:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete task
curl -X DELETE http://3.236.198.195:5000/tasks/1
