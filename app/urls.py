from django.urls import path

from .views import health, user, vendor, store, product

urlpatterns = [
    # Users
    path('user/all', user.user, name="user-all"),
    path('user/register', user.createUser, name="user-Create"),
    path('user/<int:id>/delete', user.removeUser, name="user-Delete"),
    path('user/login', user.user_login, name="user-Login"),


    # Vendors
    path('vendor/create', vendor.create_vendor_with_employee, name="vendor-Create"),
    path('vendor/all', vendor.get_all_vendors, name="vendor-get-all"),

    # Employees
    path('employee/all', vendor.get_all_vendor_employees, name="employee-get-all"),
    path('employee/create', vendor.create_employee, name="employee-create"),
    path('employee/<int:id>/get', vendor.get_employee, name="employee-get-one"),
    path('employee/<int:id>/delete', vendor.delete_employee, name="employee-delete"),
    path('employee/login', vendor.employee_login, name="employee-login"),
    path('employee/<int:id>/edit-role', vendor.edit_employee_role, name="employee-edit-role"),

    # Stores
    path('store/create', store.add_store, name="store-create"),
    path('store/all', store.get_all_stores, name="store-get-all"),
    path('store/<int:id>/get', store.get_single_store, name="store-get-one"),
    path('store/<int:id>/delete', store.delete_store, name="store-delete"),

    # Products
    path('product/all', product.get_all_products, name="product-get-all"),
    path('product/<int:id>/get', product.get_single_product, name="product-get-one"),
    path('product/create', product.add_product, name="product-create"),
    # this will delete the parent product
    path('product/<int:id>/delete', product.delete_product, name="product-delete-base"),


    # Products in Store
    path('store/<int:store_id>/product/<int:product_id>/add', product.add_product_in_store, name="store-product-create"),
    # this will delete product in store
    path('store/<int:store_id>/product/<int:product_id>/delete', product.delete_product_in_store,
         name="store-product-delete"),

    # get single product in store
    path('store/<int:store_id>/product/<int:product_id>/get', product.get_single_store_product,
         name="store-product-get-one"),

    # update product units
    path('store/<int:store_id>/product/<int:product_id>', product.update_product_availability,
         name="product-get-all-store-get-all"),

    # get all product in store
    path('store/<int:store_id>/products', product.get_all_products_in_store,
         name="store-product-get-all"),

    # get all store for one product
    path('product/<int:product_id>/stores', product.get_product_availability_in_store,
         name="product-store-get-all"),

    # all products all store
    path('stores/products', product.get_all_products_all_stores,
         name="product-get-all-store-get-all"),


    #Health
    path('', health.check_health)
]