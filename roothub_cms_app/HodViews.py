from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from .models import Admin, Courses, CustomUser, Trainee, Trainers


def admin_home(request):
    admin = Admin.objects.all()
    return render(request,"hod_template/home_content.html", {"admin":admin})

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method !="POST":
        return HttpResponseRedirect("error_404")
    else:
        try:
            first_name = request.POST.get("first_name").capitalize()
            middle_name = request.POST.get("middle_name").capitalize()
            last_name = request.POST.get("last_name").capitalize()
            email = request.POST.get("email").lower().replace(' ', '')
            password = request.POST.get("password")
            username = request.POST.get("username").replace(' ', '')
            gender = request.POST.get("gender")
            address = request.POST.get("address")
            religion = request.POST.get("religion")
            state = request.POST.get("state")
            country = request.POST.get("country")

            if email=="" and CustomUser.objects.filter(email=""):
                pass
            else:
                if CustomUser.objects.filter(email__iexact=email).exists():
                    messages.error(request, "Email already exists!")
                    return render(request, 'hod_template/add_staff_template.html')

            
            if not password:
                messages.error(request, "Your Password must not be empty")
                if len(password) <= 7:
                    messages.error(request, "Password must be more than 7 letters long!")
                    return render(request, 'hod_template/add_staff_template.html')
            
            elif CustomUser.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username already exists!")
                return render(request, 'hod_template/add_staff_template.html')
            
            elif not first_name:
                messages.error(request, "Your First Name and your must not be empty")
                if not last_name:
                    messages.error(request, "Your Last Name must not be empty")
                    if not username:
                        messages.error(request, "Your Username must not be empty")
                        if not gender:
                            messages.error(request, "Select your Gender")
                        return render(request, 'hod_template/add_staff_template.html')
            
            else:
      
                user = CustomUser.objects.create_user(
                    first_name = first_name,
                    middle_name = middle_name,
                    last_name =last_name,
                    email =email,
                    password =password,
                    username=username,
                    gender =gender,
                    address =address,
                    religion =religion,
                    state =state,
                    country =country,
                    user_type = 2
                )
                user.save()
                messages.success(request, "Staff Added Successfully")
                return HttpResponseRedirect("admin_home")
        except Exception as e:
            print(e)
            messages.error(request, "An unexpected error occured")
            return HttpResponseRedirect("add_staff")

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
    return render(request,"hod_template/view_trainer.html" ,{"trainer": trainers})

def view_course(request):
    course = Courses.objects.all()
    return render(request,"hod_template/view_course.html" ,{"course": course})

def view_trainee(request):
    trainees = Trainee.objects.all()
    return render(request,"hod_template/view_trainee.html" ,{"trainee": trainees})

def edit_trainer(request,trainer_id):
    trainer = Trainers.objects.get(admin=trainer_id)