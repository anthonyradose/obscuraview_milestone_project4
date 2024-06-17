const countrySelect = document.getElementById('id_default_country');

let countrySelected = countrySelect.value;

if (!countrySelected) {
    countrySelect.style.color = '#aab7c4';
}

countrySelect.addEventListener('change', function() {
    countrySelected = this.value;
    if (!countrySelected) {
        this.style.color = '#aab7c4';
    } else {
        this.style.color = '#000';
    }
});
