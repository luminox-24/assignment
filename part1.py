from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
import mysql.connector

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'due date':fields.String(required=True, description='The task details'),
    'status':fields.String(default='Not started',required=True, description='Not started, In progress, and Finished')
})

mydb = mysql.connector.connect(host='localhost',user='yog',passwd='1234',database='yog',autocommit=True)    
   
mycursor = mydb.cursor()
#mycursor.execute("DELETE FROM tasks") 

class TodoDAO(object):
    def __init__(self):
        self.todos = []
        mycursor.execute("SELECT id FROM tasks ORDER BY ID DESC LIMIT 1")
        for i in mycursor:
            self.counter=i[0];
        

    def get(self, id):
        '''for todo in self.todos:
            if todo['id'] == id:
                return todo'''
        out=list()
        insert_stmnt=("SELECT * FROM TASKS WHERE id=%s")
        val=(id,)
        mycursor.execute(insert_stmnt,val)
        for i in mycursor:
            out.append({'id':i[0],'task':i[1],'due date':i[2],'status':i[3]})
        return out
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        insert_stmnt=("INSERT INTO TASKS VALUES (%s,%s,%s,%s)")
        val=(todo['id'],todo['task'],todo['due date'],todo['status'])
        mycursor.execute(insert_stmnt,val)
        #mydb.commit()
        self.todos.append(todo)
        return todo
    @ns.marshal_with(todo)
    def update(self, id, data):
        todo=data
        insert_stmnt=("UPDATE TASKS SET tasks=%s,due_date=%s,status=%s WHERE id=%s")
        val=(data['task'],data['due date'],data['status'],id)
        mycursor.execute(insert_stmnt,val)
        #mydb.commit()
        return todo
        
    

    def delete(self, id):
        insert_stmnt=("DELETE FROM TASKS WHERE id=%s")
        val=(id,)
        mycursor.execute(insert_stmnt,val)
        #mydb.commit()
        return {'task':'deleted'}


DAO = TodoDAO()
#DAO.create({'task': 'Build an API'})
#DAO.create({'task': '?????'})
#DAO.create({'task': 'profit!'})
#DAO.create({'task': 'clean car','due date': '2021-05-31','status': 'finished'})

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    #@ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        out=list()
        mycursor.execute("SELECT * FROM TASKS")
        for i in mycursor:
            out.append({'task':i[1],'due date':i[2].strftime("%Y-%m-%d"),'status':i[3]})
        return out

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)



@ns.route('/finished')
@ns.response(404, 'Todo not found')
class statusCheckFinished(Resource):
    '''this gets all tasks which are finished'''
    def get(self):
        out=list()
        mycursor=mydb.cursor()
        mycursor.execute("SELECT tasks,due_date FROM TASKS WHERE status='finished'")
        for i in mycursor:
            out.append({'task':i[0]})
        return out

@ns.route('/overdue')
@ns.response(404, 'Todo not found')
class statusCheckOverdue(Resource):
    '''this gets all tasks which are past their due date, as of the date this query is run'''
    def get(self):
        out=list()
        mycursor.execute("SELECT tasks FROM TASKS WHERE due_date<curdate() AND status!='finished'")
        for i in mycursor:
            out.append({'task':i[0]})
        return out
    
@ns.route('/<string:due_date>')
@ns.response(404, 'Todo not found')
@ns.param('due_date', 'The due date of the task')
class dueDate(Resource):
    '''this gets a list of tasks which are due to be finished on that specified date'''
    def get(self,due_date):
        out=list()
        val=(due_date,)
        insert_stmt=("SELECT tasks FROM TASKS WHERE due_date=%s")
        mycursor.execute(insert_stmt,val)
        for i in mycursor:
            out.append({'task':i[0]})
        return out            



if __name__ == '__main__':
    app.run(debug=True)
