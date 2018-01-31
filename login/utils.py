from .models import File

# check if the file is shared to the user
# file_name -> name of the file -- can be easy updated to the path of file
# user -> django user trying to access the file
# returns boolean shared -> True if shared to user
def shared_file(file_name, user):
	shared = False
	try:
		File.objects.get(file_name=file_name,users=user)
		shared = True
	except:
		pass
	return shared