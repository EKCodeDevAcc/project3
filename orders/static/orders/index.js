
function addToCart(item_type, item_name, item_price, item_size, item_pizza_topping, item_sub_topping) {

    $.ajax({
        url: '/addCart',
        data: {
            itemtype: item_type,
            itemname: item_name,
            itemprice: item_price,
            itemsize: item_size,
            itempizzatopping: item_pizza_topping,
            itemsubtopping: item_sub_topping
        },
        success: function(data){
            location.reload();
        }
    });
};

function removeCart(item_id) {
    $.ajax({
        url: '/removeCart',
        data: {
            itemid: item_id,
        },
        success: function(data){
            location.reload();
        }
    });
};

function checkoutCart(order_price){
    var float_price = parseFloat(order_price).toFixed(2);

    $.ajax({
        url: '/checkoutCart',
        data: {
            orderprice: float_price,
        },
        success: function(data){
            alert("Thank you for choosing Pinocchio's Pizza & Subs!");
            window.location = "/myOrders";
        }
    });
};

function addPizzaToppings(item_type, item_name, item_price, item_size, topping_size) {

    if (topping_size == 0) {
        addToCart(item_type, item_name, item_price, item_size, '', '');
    } else {
        // Get the modal
        var modal = document.getElementById('pizzaModal');

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks on the button, open the modal
        modal.style.display = "block";

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
            location.reload();
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                location.reload();
            }
        }

        const topping_message = document.createElement('h4');
        topping_message.innerHTML = "Please select " + topping_size + " toppings.";

        document.querySelector('#topping_message').append(topping_message);

        //If number of checked checkboxes are equal to the number of toppings, deny checking current checkbox
        $(document).ready(function() {
            $('input.topping_check').on('change', function(evt) {
                if ($(this).siblings(':checked').length == topping_size) {
                    this.checked = false;
                }
            });
        });

        var select_button = document.querySelector('#topping_complete');
        var total_topping_length = document.querySelector('#total_topping_length').innerHTML;

        select_button.onclick = function() {
            var unchecked_length = $("input:checkbox[class=topping_check]:not(:checked)").length;
            var checked_length = total_topping_length - unchecked_length;

            if (topping_size > 0) {
                if (checked_length != topping_size) {
                    alert("Please select " + topping_size + " toppings.");
                } else {
                    var final_toppings = new Array();
                    var checked = document.querySelector('.topping_check:checked').value;

                    $(document).ready(function() {
                        $("input:checkbox[class=topping_check]:checked").each(function(){
                            final_toppings = final_toppings + $(this).val() + ', ';
                        });
                    });
                    final_toppings = final_toppings.substring(0, final_toppings.length - 2);
                }
            } else {
                final_toppings = "";
            }

            addToCart(item_type, item_name, item_price, item_size, final_toppings, '');
        }
    };
};

function addSubsToppings(item_type, item_name, item_price, item_size, topping_size) {

    var mushrooms = document.getElementById('Mushrooms');
    var pmushrooms = document.getElementById('p_Mushrooms');
    var green_peppers = document.getElementById('Green Peppers');
    var pgreen_peppers = document.getElementById('p_Green Peppers');
    var onions = document.getElementById('Onions');
    var ponions = document.getElementById('p_Onions');

    if (item_name != 'Steak + Cheese'){
        mushrooms.style.display = "none";
        pmushrooms.style.display = "none";
        green_peppers.style.display = "none";
        pgreen_peppers.style.display = "none";
        onions.style.display = "none";
        ponions.style.display = "none";
    }

    // Get the modal
    var modal = document.getElementById('subsModal');

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
        location.reload();
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            location.reload();
        }
    }

    var select_button = document.querySelector('#sub_topping_complete');
    var total_topping_length = document.querySelector('#sub_topping_length').innerHTML;

    select_button.onclick = function() {
        var unchecked_length = $("input:checkbox[class=sub_topping_check]:not(:checked)").length;
        var checked_length = total_topping_length - unchecked_length;

        if (checked_length == 0) {
            final_toppings = "";
        } else {
            var final_toppings = new Array();
            var checked = document.querySelector('.sub_topping_check:checked').value;

            $(document).ready(function() {
                $("input:checkbox[class=sub_topping_check]:checked").each(function(){
                    final_toppings = final_toppings + $(this).val() + ', ';
                });
            });
            final_toppings = final_toppings.substring(0, final_toppings.length - 2);

            var extra = checked_length * .5;
            var float_item = parseFloat(item_price);
            item_price = float_item + extra;
        }

        addToCart(item_type, item_name, item_price, item_size, '', final_toppings);
    }
};

function changeOrderStatus(order_status, order_length) {
    var unchecked_length = $("input:checkbox[class=change_order_status]:not(:checked)").length;
    var checked_length = order_length - unchecked_length;

    if (checked_length > 0) {
        var final_orders = new Array();
        var checked = document.querySelector('.change_order_status:checked').value;

        $(document).ready(function() {
            $("input:checkbox[class=change_order_status]:checked").each(function(){
                final_orders = final_orders + $(this).val() + ', ';
            });
        });
        final_orders = final_orders.substring(0, final_orders.length - 2);

        $.ajax({
            url: '/changeOrderStatus',
            data: {
                orderstatus: order_status,
                finalorders: final_orders
            },
            success: function(data){
                location.reload();
            }
        });
    } else {
        alert("Please select at least one item to change its status!");
    }
}

function selectOrderDetails(order_id) {
    $.ajax({
        url: '/orderDetails',
        data: {
            orderid: order_id
        },
        success: function(data) {
            // Get the modal
            var modal = document.getElementById('orderModal');

            // Get the <span> element that closes the modal
            var span = document.getElementsByClassName("close")[0];

            // When the user clicks on the button, open the modal
            modal.style.display = "block";

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
                location.reload();
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                    location.reload();
                }
            }

            var total_price = 0;

            for (var i=0; i<data.length; i++) {

                const details = Object.values(data[i])

                const newTr = document.createElement('tr');

                const menu_type = document.createElement('td');
                menu_type.innerHTML = details[2].item_type;
                newTr.append(menu_type);

                const menu_name = document.createElement('td');
                menu_name.innerHTML = details[2].item_menu_name;
                newTr.append(menu_name);

                const menu_size = document.createElement('td');
                menu_size.innerHTML = details[2].item_size;
                newTr.append(menu_size);

                const menu_topping = document.createElement('td');
                if (details[2].topping_pizza != '') {
                    menu_topping.innerHTML = details[2].topping_pizza;
                } else if (details[2].topping_sub != '') {
                    menu_topping.innerHTML = details[2].topping_sub;
                } else {
                    menu_topping.innerHTML = '';
                }
                newTr.append(menu_topping);

                const menu_price = document.createElement('td');
                menu_price.innerHTML = '$ ' + details[2].item_price;
                newTr.append(menu_price);

                const menu_status = document.createElement('td');
                menu_status.innerHTML = details[2].item_status;
                newTr.append(menu_status);

                document.querySelector('#order_details').append(newTr);

                total_price = total_price + details[2].item_price;
            }

            const costDiv = document.createElement('h4');
            costDiv.innerHTML = 'Total Price: $ ' + total_price;
            costDiv.className = 'total_cost'
            document.querySelector('#order_total_price').append(costDiv);

        }
    });
}