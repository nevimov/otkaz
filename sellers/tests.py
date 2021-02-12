from django.test import TestCase

# Ensure that:
#
# * Anonymous users redirected to the login page, if they try to access any
#   page of the seller admin.
#
# * Sellers CAN access the seller admin.
#
# * Seller can add a new window.
# * Seller can edit an existing window.
# * Seller sees a list of existing windows, if there any.
#
# * Seller can't publish windows util he adds required contact info (at least
#   one Place and one Phone).
#