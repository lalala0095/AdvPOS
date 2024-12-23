from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route('/products_records', methods=['GET', 'POST'])
@login_required
def products():
    db = current_app.db
   
    # Fetch all products records from the database
    products_records = list(db.products.find())
    return render_template('products.html', products_records=products_records)


@products_blueprint.route('/products_add', methods=['GET', 'POST'])
@login_required
def products_add():
    db = current_app.db
    if request.method == 'POST':
        # Add a new products record
        date_inserted = datetime.now()
        count_of_product_existing = str(db['products'].count_documents({}))
        product_id = count_of_product_existing.zfill(6)
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        product_type = request.form.get('product_type')

        if product_name and price:
            new_record = {
                "date_inserted": date_inserted,
                "product_id": int(product_id),
                "product_name": product_name,
                "product_type": product_type,
                "price": float(price),
            }
            db.products.insert_one(new_record)
            flash("Product record added successfully!", "success")
        else:
            flash("All fields are required!", "danger")

        return redirect(url_for('products_blueprint.products_add'))

    # Fetch all products records from the database
    products_records = list(db.products.find())
    return render_template('products_add.html', products_records=products_records)



# Route to delete a products record
@products_blueprint.route('/products_delete/<string:record_id>', methods=['POST'])
@login_required
def products_delete(record_id):
    db = current_app.db
    try:
        db.products.delete_one({"_id": ObjectId(record_id)})
        flash("products record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('products_blueprint.products'))

@products_blueprint.route('/products_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def products_edit(record_id):
    db = current_app.db
    record = db.products.find_one({"_id": ObjectId(record_id)})
    products = list(db.products.find())

    if not record:
        flash("products record not found!", "danger")
        return redirect(url_for('products_blueprint.products'))

    if request.method == 'POST':
        date_inserted = request.form.get('date_inserted')
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        product_type = request.form.get('product_type')
        date_updated = datetime.now()

        if product_name and product_id:
            updated_record = {
                "date_inserted": date_inserted,
                "product_id": int(product_id),
                "product_name": product_name,
                "product_type": product_type,
                "price": float(price),
                "date_updated": date_updated
            }
            try:
                db.products.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
                flash("products record updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating record: {e}", "danger")
            return redirect(url_for('products_blueprint.products'))

        flash("All fields are required!", "danger")

    return render_template('products_edit.html', record=record, products=products)