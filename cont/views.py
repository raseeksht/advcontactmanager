from django.http import HttpResponse
from django.shortcuts import render
from contacts.models import Contact

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
  return HttpResponse("login page ho yo")
  
def lists(request):
  values = {"contacts":getContacts(),"address":getAddress(),"list_active":"active"}
  return render(request,"lists.html",values)

def add(request):
  values = {"title":"Add Contacts","address":getAddress(),"add_active":"active"}
  return render(request,"add.html",values)
  

def filter(request):
  if request.method == "POST":
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
  return HttpResponse("ok here we are")


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









