from django.http import HttpResponse
from django.shortcuts import render,redirect
from contacts.models import Contact
from django.contrib.auth import authenticate,login

def getContacts():
  return Contact.objects.all()

def getAddress():
  '''
  :parameters: not needed
  :return: set of contacts (not repeated)
  '''
  address = set(each.address for each in getContacts())
  return address

def index(request):
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect("/lists/")
    else:
      return HttpResponse("incorrect email or password")
    return HttpResponse(f"<h1>we got post request here</h1>username: {username}<br>password: {password}")
  values = {"nonav":True}
  return render(request,"index.html",values)
  
def lists(request):
  print(request.user.is_authenticated)
  if request.user.is_authenticated:
    values = {"contacts":getContacts(),"address":getAddress(),"list_active":"active"}
    return render(request,"lists.html",values)
  else:
    #return HttpResponse("/")
    return redirect("/")
    
def add(request):
  if request.user.is_authenticated:
    values = {"title":"Add Contacts","address":getAddress(),"add_active":"active"}
    return render(request,"add.html",values)
  else:
    return redirect("/")

def filter(request):
  if request.method == "POST" and request.user.is_authenticated:
    addr= request.POST["address"]
    res = Contact.objects.filter(address=addr)
    string = """
    <table class="table table-striped">
    <tr>
    <td>name</td>
    <td>number</td>
    <td>address</td>
    </tr>
    """
    for each in res:
      string += f"""
      <tr>
        <td>{each.name}</td>
        <td>{each.number}</td>
        <td>{each.address}</td>
      </tr>"""
    string += """</table>"""
    return HttpResponse(string)
  elif request.method == "GET":
    return redirect("/")
  return HttpResponse("make sure that you are valid user")


def alert(msg):
  return f"""<div class="alert alert-warning alert-dismissible fade show" role="alert">
  <strong>{msg}</strong>
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>"""

def addData(request):
  if request.method == "POST":
    name1 = request.POST["name"]
    number1 = request.POST["number"]
    address1 = request.POST["address"]
    newContact = Contact(name=name1,number=number1,address=address1)
    newContact.save()
    return HttpResponse(alert(f"Added ({name1},{number1},{address1})"))
  return HttpResponse("make post request")



def needForEdit(request):
  if request.method == "POST" and request.user.is_authenticated:
    return HttpResponse("okay you are good to go")
  else:
    return HttpResponse("this is either get request or you are not a valid user")

def editContact(request):
  if request.method == "POST" and request.user.is_authenticated:
    sn = request.POST["sn"]
    name = request.POST["name"]
    number = request.POST["number"]
    address = request.POST["address"]
    editCont = Contact.objects.get(id=sn)
    editCont.name = name
    editCont.number = number
    editCont.address = address
    editCont.save()
    print("saved")
    return HttpResponse(name+str(sn)+" received")

def deleteContact(request):
  if request.method=="POST" and request.user.is_authenticated:
    sn,name,number,address = getContactDetailsFromRequest(request)
    try:
      getInfo = Contact.objects.get(id=sn,name=name,number=number,address=address)
    except Exception:
      return HttpResponse("do not edit if you want to delete..")
    getInfo.delete()
    return HttpResponse("done")
    
def getContactDetailsFromRequest(request):
  sn = request.POST["sn"]
  name = request.POST["name"]
  number = request.POST["number"]
  address = request.POST["address"]
  return sn,name,number,address