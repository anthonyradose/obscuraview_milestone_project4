const stripe_public_key = document
  .getElementById("id_stripe_public_key")
  .textContent.slice(1, -1);
const client_secret = document
  .getElementById("id_client_secret")
  .textContent.slice(1, -1);
  console.log("Stripe Public Key:", stripe_public_key);
  console.log("Client Secret:", client_secret);
const stripe = Stripe(stripe_public_key);
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
card.mount("#card-element");

const error_div = document.getElementById("card-errors");
// Handle realtime validation errors on the card element
card.addEventListener("change", function (event) {
  if (event.error) {
    let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
    error_div.innerHTML = html;
  } else {
    error_div.textContent = "";
  }
});

const form = document.getElementById("payment-form");
const submit_button = document.getElementById("submit-button");

form.addEventListener("submit", function (ev) {
  ev.preventDefault();
  card.update({ disabled: true });
  submit_button.disabled = true;

  stripe
    .confirmCardPayment(client_secret, {
      payment_method: {
        card: card,
      },
    })
    .then(function (result) {
      if (result.error) {
        let html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
        error_div.innerHTML = html;
        card.update({ disabled: false });
        submit_button.disabled = false;
      } else {
        if (result.paymentIntent.status === "succeeded") {
          form.submit();
        }
      }
    });
});
