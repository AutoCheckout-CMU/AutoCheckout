import BookKeeper

# print all products from a certain shelf
gondola_id = 1
shelf_id = 5
# plate_id = 5

product_ids = BookKeeper.getProductIDsFromPosition(gondola_id, shelf_id)
for product_id in product_ids:
    product = BookKeeper.getProductByID(product_id)
    print (product)