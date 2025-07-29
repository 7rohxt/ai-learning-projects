window.onload = async () => {
    const res = await fetch('/get_ocean_proximity');
    const options = await res.json();

    const select = document.getElementById('ocean-proximity');
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.text = opt;
        select.appendChild(option);
    });
};

const form = document.getElementById('predict-form');
const result = document.getElementById('result');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    for (let key in data) {
        if (!isNaN(data[key])) {
            data[key] = Number(data[key]);
        }
    }

    const res = await fetch('/predict_price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const json = await res.json();

    if (json.predicted_price !== undefined) {
        result.innerText = `Predicted Price: $${json.predicted_price}`;
    } else {
        result.innerText = `Error: ${json.error}`;
    }
});