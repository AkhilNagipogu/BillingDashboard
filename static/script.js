let items = [];
let total = 0;

function add() {
    const select = document.getElementById('product');
    const name = select.options[select.selectedIndex].text;
    const price = Number(select.value);
    const qty = Number(document.getElementById('qty').value);

    items.push({ name, price, qty });
    total += price * qty;

    document.getElementById('list').innerHTML +=
        `<li>${name} x ${qty}</li>`;

    document.getElementById('total').innerText = total;
}

function generateBill() {
    fetch('/generate-bill', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items, total })
    })
    .then(res => res.json())
    .then(data => {
        const img = document.getElementById('qrImage');
        img.src = '/' + data.qr;
        img.style.display = 'block';
    });
}

