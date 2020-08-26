#This decorator will be used to modify our class UI_mainwindow by adding methods
#The methods are given as arguments to the add_methods_to_class.
#They are then added to the class using the setattr command

def add_methods_to_class(methods):
	def class_decorator(Class):
		for method in methods:
			setattr(Class, method.__name__, method)
		return Class
	return class_decorator
		