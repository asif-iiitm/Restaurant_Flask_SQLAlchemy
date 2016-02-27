from flask import Flask, render_template ,request , redirect , url_for , flash, jsonify
app=Flask(__name__)

"""
SQLAlchemy 
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Restaurant , MenuItem

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession=sessionmaker(bind=engine)
session=DBSession()

#Make API Endpoint (GET Request)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurante=session.query(Restaurant).filter_by(id=restaurant_id).one()
	itemse = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html',restaurant=restaurante,items=itemse)
	# output=''
	# for i in items:
	# 	output+=i.name
	# 	output+='</br>'
	# 	output+=i.price
	# 	output+='</br>'
	# 	output+=i.description
	# 	output+='</br>'
	# return output

#Task 1 add new menu item

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method=='POST':
		newItem=MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created! ")
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	#return "Task1"
	else:
		return render_template('newmenuitem.html',restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
	editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method=='POST':
		if request.form['name']:
			editedItem.name=request.form['name']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,i=editedItem)	






	return "Task2"
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id,menu_id):
	return "Task3"

if __name__ == '__main__':
	app.secret_key='super_secret_key'
	app.debug=True
	app.run(host='0.0.0.0', port=5000)