from google.cloud import datastore

def create_client(project_id):
    return datastore.Client(project_id)

def add_task(client, description):
    key = client.key('Task')
    task = datastore.Entity(
        key, exclude_from_indexes=['description'])
    task.update({
        'created': datetime.datetime.utcnow(),
        'description': description,
        'done': False
    })
    client.put(task)
    return task.key

def mark_done(client, task_id):
    with client.transaction():
        key = client.key('Task', task_id)
        task = client.get(key)
        if not task:
            raise ValueError(
                'Task {} does not exist.'.format(task_id))
        task['done'] = True
        client.put(task)
