from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<int:item_id>",views.show,name = "show_item"),
    path("watch/<int:item_id>",views.watchlist_add,name = "watchlist"),
    path("<int:item_id>/#",views.watchlist_remove,name ="watchlistrm"),
    path("<str:user>/watchlist",views.watchlist_viewing,name="view_watchlist"),
    path("create_listing",views.listing,name = "create_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>",views.biding,name="bids")
]
