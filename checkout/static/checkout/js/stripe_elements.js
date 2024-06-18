const stripePublicKey = document
  .getElementById("id_stripe_public_key")
  .textContent.slice(1, -1);
console.log(stripePublicKey);
const clientSecret = document
  .getElementById("id_client_secret")
  .textContent.slice(1, -1);
console.log(clientSecret);
const stripe = Stripe(stripePublicKey);
console.log(stripe);
const elements = stripe.elements();

const style = {
  base: {
    color: "#000",
    fontFamily: '"Roboto", sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#dc3545",
    iconColor: "#dc3545",
  },
};
const card = elements.create("card", { style: style });
console.log(card);
card.mount("#card-element");

// Handle realtime validation errors on the card element
card.addEventListener("change", function (event) {
  const errorDiv = document.getElementById("card-errors");
  if (event.error) {
    let html = `
            <span class="icon" role="alert">
                <i class="bi bi-x"></i>
            </span>
            <span>${event.error.message}</span>
        `;
    errorDiv.innerHTML = html;
  } else {
    errorDiv.textContent = "";
  }
});

// Handle form submit
const form = document.getElementById("payment-form");
console.log(form);
form.addEventListener("submit", function (ev) {
  ev.preventDefault();

  card.update({ disabled: true });

  document.getElementById("submit-button").setAttribute("disabled", true);

  document.getElementById("payment-form").style.display = "none";

  document.getElementById("loading-overlay").style.display = "block";

  const saveInfo = document.getElementById("id-save-info").checked;
  console.log(saveInfo);
  // From using {% csrf_token %} in the form
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  console.log(csrfToken);
  const postData = {
    csrfmiddlewaretoken: csrfToken,
    client_secret: clientSecret,
    save_info: saveInfo,
  };
  console.log(postData);
  const url = "/checkout/cache_checkout_data/";
  console.log(url);
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(postData),
  })
    .then((response) => response.json())
    .then(() => {
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: {
              name: form.full_name.value.trim(),
              phone: form.phone_number.value.trim(),
              email: form.email.value.trim(),
              address: {
                line1: form.street_address1.value.trim(),
                line2: form.street_address2.value.trim(),
                city: form.town_or_city.value.trim(),
                country: form.country.value.trim(),
                state: form.county.value.trim(),
              },
            },
          },
          shipping: {
            name: form.full_name.value.trim(),
            phone: form.phone_number.value.trim(),
            address: {
              line1: form.street_address1.value.trim(),
              line2: form.street_address2.value.trim(),
              city: form.town_or_city.value.trim(),
              country: form.country.value.trim(),
              postal_code: form.postcode.value.trim(),
              state: form.county.value.trim(),
            },
          },
        })
        .then(function (result) {
          if (result.error) {
            const errorDiv = document.getElementById("card-errors");
            let html = `
                <span class="icon" role="alert">
                <i class="bi bi-x"></i>
                </span>
                <span>${result.error.message}</span>`;
            errorDiv.innerHTML = html;
            document.getElementById("payment-form").style.display = "block";
            document.getElementById("loading-overlay").style.display = "none";
            card.update({ disabled: false });
            document
              .getElementById("submit-button")
              .removeAttribute("disabled");
          } else {
            if (result.paymentIntent.status === "succeeded") {
              form.submit();
            }
          }
        });
    })
    .catch(() => {
      location.reload();
    });
});
