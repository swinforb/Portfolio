import MySQLdb
import flask, datetime
from flask import render_template, request, redirect, flash
import configparser

def read_mysql_config(mysql_config_file_name):
    config = configparser.ConfigParser()
    config.read(mysql_config_file_name)
    return dict(config['client'])


# This will be different for each user.
config_info = read_mysql_config("/nfs/stak/users/swinforb/.my.cnf")

# db_conn = MySQLdb.connect(config_info['host'],
#                           config_info['user'],
#                           config_info['password'],
#                           config_info['database'])

db_conn = [config_info[k] for k in ['host', 'user', 'password', 'database']]

def db_conn_func():
    return MySQLdb.connect(*db_conn)

def purchases_helper():
    conn = db_conn_func()
    cursor = conn.cursor()
    # get the list of current customers
    cursor.execute("SELECT first_name, last_name FROM Customers;")
    customers = cursor.fetchall()
    # add customers to a list and format   
    customer_list = []
    for customer in customers:
        customer = str(customer).strip("()").replace("'", "").replace(",", '')
        customer_list.append(customer) 
     # get the list of current cashiers

    cursor.execute("SELECT DISTINCT first_name, last_name FROM Cashiers;")
    cashiers = cursor.fetchall()
    # add customers to a list and format   
    cashiers_list = []
    for cashier in cashiers:
        cashier = str(cashier).strip("()").replace("'", "")
        
        cashiers_list.append(cashier) 

    cursor.execute("SELECT product_name FROM Products;")
    products = cursor.fetchall()
    products_list = []
    
    for p in products:
        p = str(p).strip("()").replace("'", "").replace(",", '')
        products_list.append(p)
    cursor.execute("SELECT * FROM Purchases;")
    all_info = cursor.fetchall()
    return (all_info, customer_list, cashiers_list, products_list)


# -----------------------------------------------------------------
webapp = flask.Flask(__name__, static_url_path='/static')

# Home
@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/customers/')
def customers():
    conn = db_conn_func()
    cursor = conn.cursor()
    cursor.execute("SELECT reward_id FROM Rewards;")
    result1 = cursor.fetchall()
    reward_id_list = []
    for i in result1:
        reward_id_list.append(i[0]) 
    option = f"<option value=[i]</option>"
    cursor.execute("SELECT * FROM Customers;")
    result2 = cursor.fetchall()
    return render_template('customers.html', customer_info=result2, reward_options=reward_id_list, option=option)

@webapp.route('/purchases/')
def Purchases():
    results = purchases_helper()
    all_info = results[0]
    customer_list = results[1]
    cashiers_list = results[2]
    products = results[3]
    print(products)
    return render_template('purchases.html', rows=all_info, customers=customer_list, cashiers=cashiers_list, products=products)

@webapp.route('/products/')
def products():
    conn = db_conn_func()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products;")
    result = cursor.fetchall()
    print(result)

    return render_template('products.html', rows=result)

@webapp.route('/cashiers/')
def cashiers():
    conn = db_conn_func()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cashiers;")
    result = cursor.fetchall()
    return render_template('cashiers.html', cashier_info=result)

@webapp.route('/rewards/')
def rewards():
    conn = db_conn_func()
    cursor = conn.cursor()
    selectquery = "SELECT * FROM Rewards;"
    cursor.execute(selectquery, ())
    # conn.commit()
    result = cursor.fetchall()
    return render_template('rewards.html', rewards_info=result)

@webapp.route('/purchases_products/')
def purchases_products():
    return render_template('purchases_products.html')

# handle submitted forms
@webapp.route('/customer_results', methods=['GET', 'POST'])
def customer_results():
    # result = ''
    conn = db_conn_func()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers;")
    result = cursor.fetchall()

    cursor.execute("SELECT reward_id FROM Rewards;")
    result1 = cursor.fetchall()
    reward_id_list = []
    for i in result1:
        reward_id_list.append(i[0]) 
    option = f"<option value=[i]</option>"


    # if insert button is pressed, insert the provided info
    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Customers (first_name, \
                                                last_name,\
                                                customer_phone,\
                                                customer_email,\
                                                reward_id) \
                                                VALUES (%s,%s,%s,%s, %s);"
        # get the text entered from the website
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        reward_id = request.form['reward_id']
        userdata = [fname, lname, phone, email, reward_id]
        index = 0
        for data in userdata:
            if data == '':
                userdata[index] = None
            index += 1
        # try the query, if something goes wrong return an error
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(insertquery, userdata)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, option=option, customer_results_error=error)

        insertedresult = f'Customer Inserted: {userdata[0]}, {userdata[1]}'
        cursor.execute("SELECT * FROM Customers;")
        result = cursor.fetchall()
        return  render_template('customers.html',  customer_info=result,reward_options=reward_id_list, option=option, customer_results=insertedresult)

    # if update button is pressed
    elif "updatebutton" in request.form:
        updatequery = "UPDATE Customers SET first_name = %s, \
                                            last_name = %s, \
                                            customer_phone = %s, \
                                            customer_email=%s, \
                                            reward_id = %s \
                                            WHERE first_name = %s and last_name = %s"

        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        if not "checknull" in request.form:
            reward_id = request.form['reward_id']
        else:
            reward_id = None                       

        updatedata = (fname, lname, phone, email, reward_id, fname, lname)
        
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(updatequery, updatedata)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args[1]}"
            return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, option=option, customer_results_error=error)
        updateresult = f"Customer Updated: {fname} {lname}"
        cursor.execute("SELECT * FROM Customers;")
        result = cursor.fetchall()
        return render_template('customers.html', customer_info=result, reward_options=reward_id_list, option=option, customer_results=updateresult)


    # if search button is pressed,
    elif "searchbutton" in request.form:
        searchquery = "SELECT * FROM Customers where first_name = %s and last_name = %s;"
        first_name = request.form['fname']
        last_name = request.form['lname']
        data = (first_name, last_name)
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(searchquery, data)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, option=option, customer_results_error=error)
        # return render_template('customers.html', customer_info=result)
        return render_template('customers.html', customer_info=result, reward_options=reward_id_list, option=option)
    return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, option=option)


@webapp.route('/cashier_results/', methods=['GET', 'POST'])
def cashier_results():
    conn = db_conn_func()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cashiers;")
    result = cursor.fetchall()

    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Cashiers (first_name, \
                                                last_name,\
                                                day_total,\
                                                day_worked,\
                                                lane) \
                                                VALUES (%s,%s,%s,%s, %s);"
        fname = request.form['fname']
        lname = request.form['lname']
        lane = request.form['selectlane']
        daytotal = (request.form['daytotal'])
        dayworked = request.form['dayworked']
        userdata = [fname, lname, daytotal, dayworked, lane]

        index = 0
        for data in userdata:
            if data == '': userdata[index] = None
            index += 1
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(insertquery, userdata)
            conn.commit()
            # result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('cashiers.html', data=error)
        insertresult = f"Cashier Added: {fname} {lname}"
        cursor.execute("SELECT * FROM Cashiers;")
        result = cursor.fetchall()
        return  render_template('cashiers.html', cashier_info=result, cashier_insert=insertresult)

    if "searchbutton" in request.form:
        searchquery = "SELECT * FROM Cashiers where (first_name = %s and last_name = %s) or day_worked = %s;"
        first_name = request.form['fname']
        last_name = request.form['lname']
        day_worked = request.form['dayworked']
        data = (first_name, last_name, day_worked)
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(searchquery, data)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('cashiers.html',  data=error)
        return  render_template('cashiers.html',  cashier_info=result)
    # if "deletebutton" in request.form:
    #     deletequery = "DELETE FROM Cashiers where cashier_id = %s;"
    #     cashier_id = request.form['cashierid']
    #     try:
    #         conn = db_conn_func()
    #         cursor = conn.cursor()
    #         cursor.execute(deletequery, cashier_id)
    #         conn.commit()
    #         result = cursor.fetchall()
    #     except Exception as e:
    #         error = f"Error: {e.args[1]}"
    #         return render_template('cashiers.html', Status=error)
    #     return render_template('cashiers.html', status=result)
    return render_template('cashiers.html', cashier_info=result)

@webapp.route('/rewards_results', methods=['POST'])
def rewards_results():
    result = ''
    result1 = ''
    conn = db_conn_func()
    cursor = conn.cursor()

    if 'insertrewards' in request.form:
        insertquery = "INSERT INTO Rewards (reward_points, reward_discount) VALUES (%s,%s);"
        reward_points = int(request.form['rewardpoints'])
        reward_discount = int(request.form['selectdiscount'])
        data = (reward_points, reward_discount)
        
        cursor.execute(insertquery, data)
        conn.commit()

    if 'deletebutton' in request.form:
        reward_id =request.form.get('deletereward')
        reward_id = (reward_id,)
        deletequery = "DELETE FROM Rewards WHERE reward_id = %s"
        try:
    
            cursor.execute(deletequery, reward_id)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args}" 
            return render_template('/rewards.html', delete_status=error )
        result1 = f"Reward Deleted: {reward_id[0]}"

    selectquery = "SELECT * FROM Rewards;"
    cursor.execute(selectquery, ())
    result = cursor.fetchall()
    return render_template('/rewards.html', rewards_info=result, delete_status=result1 )

@webapp.route('/purchases_results', methods=['GET', 'POST'])
def purchases_results():
    conn = db_conn_func()
    cursor = conn.cursor()
    submitresult = ''
    deleteresult = ''
    results = purchases_helper()
    all_info = results[0]
    customer_list = results[1]
    cashiers_list = results[2]
    products_list = results[3]

    if "submitbutton" in request.form:
        
        # try to find the customer, print error if not found
        try:
            # perform a query to get customer id
            firstname = request.form['fname']
            lastname = request.form['lname']
            querycustomer = "SELECT customer_id FROM Customers WHERE first_name =%s and last_name=%s;"
            customer = (firstname, lastname)
            cursor.execute(querycustomer, customer)
            cid1 = cursor.fetchall()
            cid1 =cid1[0][0] 
        except:
            error = "Customer Not found"
            return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, purchases_result=error, products=products_list)


        # perform a query to get cashier id
        cashiername = str(request.form['selectcashier']).replace(",", '')
        querycashier = "SELECT cashier_id FROM Cashiers WHERE first_name =%s;"
        cashiername = (cashiername, )
        cursor.execute(querycashier, cashiername)
        cashierid = cursor.fetchall()
        # cashierid will be 2d tuple. ID is the first element. 
        cashierid = cashierid[0][0]

        if request.form.get('purchasecomplete'):
            complete = 1
        else:
            complete = 0
        price = request.form['totalprice']

        products_bought = []
        
        # get the list of products that were checked
        for i in  request.form.getlist('productsbought'):
            products_bought.append(i) 
        quantity= []

        # get all quantities for the products
        for i in request.form.getlist('quantity'):
            if i != '':
                quantity.append(i)

        productids = []

        # get the id's for each product
        for i in products_bought:
            i = i + "%"
            selectproduct = "SELECT product_id FROM Products WHERE product_name LIKE %s;"
            cursor.execute(selectproduct, [i])

            # this will get just the id's and put them in the results list. 
            productids.append(str(cursor.fetchall()).replace("(", "").replace(")", "").replace(',','')) 

        # return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, products=products_list)

        date = datetime.datetime.now()
        try:
            cursor.execute('INSERT INTO Purchases (date, customer_id, cashier_id, total_price, purchase_complete) VALUES (%s,%s, %s, %s, %s);', (date, cid1, cashierid, price, complete))
            conn.commit()

            # get the purchase_id that was just inserted
            cursor.execute("SELECT purchase_id FROM Purchases ORDER BY purchase_id DESC LIMIT 1;", )
            purchase_id = cursor.fetchall()
            purchase_id = purchase_id[0][0]

            # insert every product bought into the Purchases_Products table 
            for i in range(len(products_bought)):
                insertquery = "INSERT INTO Purchases_Products (purchase_id, product_id, quantity) VALUES (%s, %s, %s);"
                args = (purchase_id, productids[i], quantity[i])
                cursor.execute(insertquery, args)
                conn.commit()

        except Exception as e:
            error = f"Error: {e.args}" 
            return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, purchases_result=error, products=products_list)

        submitresult = f"Purchase Info Submitted for: {firstname} {lastname}"


    if 'searchbutton' in request.form:
        cid2 = request.form['customerid2']
        cursor.execute('SELECT * FROM Purchases WHERE customer_id = %s;', (cid2,))
        searchresult = cursor.fetchall()
        cursor.close()
        results = purchases_helper()
        customer_list = results[1]
        cashiers_list = results[2]
        products_list = results[3]
        return render_template('/purchases.html/', rows=searchresult,  customers=customer_list, cashiers=cashiers_list, purchases_result=submitresult, products=products_list)
        
    elif (request.form.get('deletebutton') == ''):
        pid2 = request.form['purchaseid2']
        cursor.execute('DELETE FROM Purchases WHERE purchase_id = %s;', (pid2,))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        deleteresult = f"Purchase Deleted: {pid2}"
    
    results = purchases_helper()
    all_info = results[0]
    customer_list = results[1]
    cashiers_list = results[2]
    products_list = results[3]
    return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, purchases_result=submitresult, products=products_list, delete_result=deleteresult)




@webapp.route('/products_results', methods=['GET', 'POST'])
def products_results():
    conn = db_conn_func()
    cursor = conn.cursor()
    if "searchbutton" in request.form:
        try:
            seachproduct = request.form['searchproduct']
            cursor.execute('SELECT * FROM Products WHERE product_name = %s;', (seachproduct,))
            result = cursor.fetchall()
            cursor.close()
            conn.commit()
            return render_template('/products.html/', rows=result)
        except Exception as e:
            error = f"Error: {e.args}" 
            print(error)
            pass

    elif "insertbutton" in request.form:
        name1 = request.form['productname1']

        price = request.form['productprice']
        stock = request.form['stock']
        type = request.form['type']

        cursor.execute('INSERT INTO Products (product_name, product_price, stock,  type) VALUES (%s, %s, %s, %s);', (name1, price, stock, type))
        result = cursor.fetchall()
        conn.commit()
    elif "deletebutton" in request.form:
        productid = request.form['deleteproduct']
        print(productid)
        productid = (productid, )
        deletequery = "DELETE FROM Products WHERE product_id = %s;"
        cursor.execute(deletequery, productid)
        conn.commit()
    cursor.execute("SELECT * FROM Products;")
    result = cursor.fetchall()
    cursor.close()
    return render_template('/products.html/', rows=result)


if __name__ == "__main__":
    webapp.run(debug=True, port=56131)
