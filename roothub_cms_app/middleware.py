# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.utils.deprecation import MiddlewareMixin

# class Custom404Middleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         if response.status_code == 404:
#             return render(request, '404_error.html', status=404)
#         return response
    
# class LoginCheckMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, *args, **kwargs):
#         modulename = view_func.__module__
#         user = request.user
#         if user.is_authenticated:
#             if user.user_type == "1":
#                 if modulename == "roothub_cms_app.HodViews":
#                     pass
#                 elif modulename == "roothub_cms_app.views" or modulename == "django.views.static":
#                     pass
#                 else:
#                     return HttpResponseRedirect("/admin_home")
#             elif user.user_type == "2":
#                 if modulename == "roothub_cms_app.Trainer_Views":
#                     pass
#                 elif modulename == "roothub_cms_app.views" or modulename == "django.views.static":
#                     pass
#                 else:
#                     return HttpResponseRedirect("/trainer_home")
#             elif user.user_type == "3":
#                 if modulename == "roothub_cms_app.Trainee_Views" or modulename == "django.views.static":
#                     pass
#                 elif modulename == "roothub_cms_app.views":
#                     pass
#                 else:
#                     return HttpResponseRedirect("/trainee_home")
#             # else:
#             #     return HttpResponseRedirect("/")
#         # else:
#             # if request.path == ("/") or request.path == ("/dologin"):
#             #     pass
#             # else:
#             #     return HttpResponseRedirect("/")