from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import Admin, Courses, CustomUser, Trainee, Trainers


def admin_home(request):
    admin = Admin.objects.all()
    return render(request,"hod_template/home_content.html", {"admin":admin})

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")
    
    
    first_name = request.POST.get("first_name").capitalize()
    middle_name = request.POST.get("middle_name").capitalize()
    last_name = request.POST.get("last_name").capitalize()
    email = request.POST.get("email").lower().replace(' ', '')
    password = request.POST.get("password")
    username = request.POST.get("username").replace(' ', '')
    gender = request.POST.get("gender")
    profile_pic = request.FILES.get('profile_pic')
    address = request.POST.get("address")
    religion = request.POST.get("religion")
    state = request.POST.get("state")
    country = request.POST.get("country")
    phone  = request.POST.get("number")

    if profile_pic:
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)
    else:
        profile_pic_url= None

    try:
        # Check if the email already exists
        if CustomUser.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'hod_template/add_staff_template.html', {'data': request.POST})

        # Check if the username already exists
        elif CustomUser.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'hod_template/add_staff_template.html', {'data': request.POST})
        
        # Validate required fields
        elif not first_name or not last_name or not username or not gender:
            messages.error(request, "Please fill all the required fields.")
            return render(request, 'hod_template/add_staff_template.html', {'data': request.POST})
        
        elif not password:
            messages.error(request, "Password must not be empty.")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")

        elif 11>len(phone)>15:
            messages.error(request,"Input an appropiate phone number")
        else:
            # Create the CustomUser instance
            user = CustomUser.objects.create_user(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,
                profile_pic=profile_pic_url,
                user_type=2  # Assuming 2 is for trainer
            )
            user.save()
            
            trainer = user.trainers 
            trainer.gender = gender
            trainer.address = address
            trainer.religion = religion
            trainer.state = state
            trainer.country = country
            trainer.phone = phone
            trainer.save()

            messages.success(request, "Staff Added Successfully")
            return HttpResponseRedirect("admin_home")  # Redirect to admin home

    except Exception as e:
        print(e)
        messages.error(request, "An unexpected error occurred")
        return HttpResponseRedirect("add_trainer")  # Redirect to add trainer page if error occurs
   

def add_course(request):
    return render(request,"hod_template/add_course.html")

def add_courses_save(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name") 
        price = request.POST.get('price', "").strip() 

        # Check for empty input
        if not course_name:
            messages.error(request, "Course name cannot be empty.")

        if not price:
            messages.error(request, "Price cannot be empty.")

        try:
            price_value = float(price)
            if price_value <= 0:
                messages.error(request, "Price must be a positive number.")

        except ValueError:
            messages.error(request, "Price must be a valid number.")

        
        # # Check for invalid characters
        # elif not course_name.replace(" ", "").isalnum():
        #     messages.error(request, "Course name must contain only letters, numbers, and spaces.")
        
        # Check for excessively long input
        if len(course_name) > 255:
            messages.error(request, "Course name is too long. Maximum length is 255 characters.")
        
        # Check for duplicates (case-insensitive)
        elif Courses.objects.filter(course_name__iexact=course_name).exists():
            messages.error(request, f"The course '{course_name}' already exists.")
    
            # Save the course to the database
        else:
            try:
                new_course = Courses.objects.create(course_name=course_name , price_name=price_value)
                new_course.save()
                messages.success(request, f"The Course: '{course_name}' has been added successfully with its corresponding price '{price}'!")
                return HttpResponseRedirect("admin_home") 
            
            # except Courses.DoesNotExist:
            #     messages.error(request, "The selected course does not exist.")
            except Exception as e:
                    # Catch any unexpected database or system errors
                    print(e)
                    messages.error(request, f"An error occurred while adding the course and price")

    else:
        # Handle invalid methods (GET, DELETE, etc.)
        messages.error(request, "Invalid action. Use the form to submit a price.")

    return render(request,"hod_template/add_course.html")

# def add_price(request):
#     # Render available courses for GET requests
#     courses = Courses.objects.all()
#     return render(request,"hod_template/add_price.html", {"courses": courses})

# def add_price_save(request):
#     if request.method == "POST":
#         course_id = request.POST.get('course')
#         price = request.POST.get('price', "").strip()

#         # Check for empty price
#         if not price:
#             messages.error(request, "Price cannot be empty.")
#             return HttpResponseRedirect("add_price")  # Correct the redirect URL

#         # Validate price format
#         try:
#             price_value = float(price)
#             if price_value <= 0:
#                 messages.error(request, "Price must be a positive number.")
#                 return HttpResponseRedirect("add_price")
#         except ValueError:
#             messages.error(request, "Price must be a valid number.")
#             return HttpResponseRedirect("add_price")

#         # Validate course selection
#         if not course_id:
#             messages.error(request, "Please select a course.")
#             return HttpResponseRedirect("add_price")

#         # Save price to database
#         try:
#             course = Courses.objects.get(id=course_id)
#             Prices.objects.create(price_name=price_value, course=course)
#             messages.success(request, f"Price '{price_value}' added successfully for course '{course.course_name}'.")
#             return HttpResponseRedirect("admin_home")  # Redirect to admin home after success
#         except Courses.DoesNotExist:
#             messages.error(request, "The selected course does not exist.")
#             return HttpResponseRedirect("add_price")
#         except Exception as e:
#             print(f"Error creating price: {e}")
#             messages.error(request, "An unexpected error occurred while adding the price. Please try again.")
#             return HttpResponseRedirect("add_price")

#     else:
#         # Handle invalid methods (GET, DELETE, etc.)
#         messages.error(request, "Invalid action. Use the form to submit a price.")
#         return HttpResponseRedirect("add_price")

def add_student(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/add_student_template.html", {"courses": courses})

def add_student_save(request):
    pass

def view_trainer(request):
    trainers = Trainers.objects.all()
    pics = CustomUser.objects.all()
    return render(request,"hod_template/view_trainer.html" ,{"trainers": trainers,"pics":pics})

def view_course(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/view_course.html" ,{"courses": courses})

def view_trainee(request):
    trainees = Trainee.objects.all()
    pics = CustomUser.objects.all()
    return render(request,"hod_template/view_trainee.html" ,{"trainees": trainees,"pics":pics})

def edit_trainer(request, trainer_id):
    try:
        trainers = get_object_or_404(Trainers, admin=trainer_id)
        return render(request, "hod_template/edit_trainer.html", {"trainers": trainers})
    except Trainers.DoesNotExist:
        messages.error(request, "Trainer not found!")
        return HttpResponseRedirect("error_404")
    
def edit_trainer_save(request, trainer_id):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")

    users = get_object_or_404(CustomUser, id=trainer_id)
    trainers = get_object_or_404(Trainers, admin=users)
    
    
    first_name = request.POST.get("first_name", "").capitalize()
    middle_name = request.POST.get("middle_name", "").capitalize()
    last_name = request.POST.get("last_name", "").capitalize()
    email = request.POST.get("email", "").lower().strip()
    password = request.POST.get("password", "")
    username = request.POST.get("username", "").strip()
    gender = request.POST.get("gender", "")
    profile_pic = request.FILES.get('profile_pic')
    address = request.POST.get("address", "")
    religion = request.POST.get("religion", "")
    state = request.POST.get("state", "")
    country = request.POST.get("country", "")
    phone = request.POST.get("number", "").strip()

    if profile_pic:
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)
    else:
        profile_pic_url = users.profile_pic

    try:


            # Check for username duplication
        if username != users.username:
            if CustomUser.objects.filter(username__iexact=username).exclude(id=users.id).exists():
                    messages.error(request, "Username already exists!")
                    return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")

            # Check for email duplication
        if email != users.email:
            if email == "":
                    messages.error(request, "Email cannot be empty!")
                    return HttpResponseRedirect(f"edit_trainer/{trainer_id}")
            elif CustomUser.objects.filter(email__iexact=email).exclude(id=users.id).exists():
                    messages.error(request, "Email already exists!")
                    return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")

            # Validate phone number length
        if not phone.isdigit() or not (11 <= len(phone) <= 15):
                messages.error(request, "Phone number must be between 11 and 15 digits!")
                return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")
            

        users.first_name = first_name
        users.middle_name = middle_name
        users.last_name = last_name
        users.email = email
        if password:
            users.set_password(password)  # Use `set_password` for security
        users.username = username
        if profile_pic:
            users.profile_pic = profile_pic_url
        else:
            users.profile_pic = users.profile_pic
        trainers.gender = gender
        trainers.address = address
        trainers.religion = religion
        trainers.state = state
        trainers.country = country
        trainers.phone = phone
        users.save()
        trainers.save()

        messages.success(request, "Trainer updated successfully!")
        return HttpResponseRedirect("/admin_home")
    except Exception as e:
                print(e)
                messages.error(request, "Failed to edit staff")
                return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")
        
def edit_course(request,course_id):
    try:
        courses = get_object_or_404(Courses, id=course_id)
        return render(request, "hod_template/edit_course.html", {"courses": courses})
    except Trainers.DoesNotExist:
        messages.error(request, "Course not found!")
        return HttpResponseRedirect("error_404")

def edit_course_save(request,course_id):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")
    
    else:
        courses = get_object_or_404(Courses, id=course_id)

        course_name = request.POST.get("course_name")
        price = request.POST.get("price")

        if not course_name:
            messages.error(request, "Course name cannot be empty.")

        if not price:
            messages.error(request, "Price cannot be empty.")

        try:
            price_value = float(price)
            if price_value <= 0:
                messages.error(request, "Price must be a positive number.")
            
            if course_name != courses.course_name:
                if CustomUser.objects.filter(course_name__iexact=course_name).exclude(id=courses.id).exists():
                    messages.error(request, "Course already exists!")
                    return HttpResponseRedirect(f"edit_trainer/{course_id}")
            
            courses.course_name = course_name
            courses.price_name = price_value
            courses.save()

            messages.success(request, f"The course'{courses.course_name}'has been successfully update to '{course_name}' with the price '{price_value}'")
            return HttpResponseRedirect("/admin_home")

        except ValueError:
            messages.error(request, "Price must be a valid number.")
            return HttpResponseRedirect(f"edit_trainer/{course_id}")
        except Exception:
            messages.error(request, "An unexpected error occured!")
            return HttpResponseRedirect(f"edit_trainer/{course_id}")

            
        
def delete_trainer(request,trainer_id):
    pass

def delete_trainer_save(request,trainer_id):
    pass
