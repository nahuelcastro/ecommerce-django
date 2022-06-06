let updateBtns = document.querySelectorAll('.update-cart');

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        console.log(this.dataset)
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId: ', productId, ', action: ', action)

        console.log('USERX: ', user)
        console.log(user === 'AnonymousUser')
        if (user === 'AnonymousUser') {
            alert('Please login to add products to your cart')
        } else {
            UpdateUserOrder(productId, action)
        }

    })
}

// function addCookieItem(productId, action) {
//     console.log('User is Anonymous, adding cookie...')

//     if (action === 'add') {
//         if (cart[productId] == undefined) {
//             cart[productId] = { 'quantity': 1 }
//         } else {
//             cart[productId]['quantity'] += 1
//         }
//     }

//     if (action === 'remove') {
//         cart[productId]['quantity'] -= 1
//         if (cart[productId]['quantity'] <= 0) {
//             delete cart[productId]
//         }
//     }

//     console.log('cart: ', cart)
//     document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=path=/'
//     location.reload()
// }

function UpdateUserOrder(productId, action) {
    console.log('User is Authenticated, sending data...')

    let url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log('data: ', data)
            location.reload()
        });
}
