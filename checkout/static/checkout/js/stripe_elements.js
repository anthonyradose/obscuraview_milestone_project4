const stripe_public_key = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
const client_secret = document.getElementById('id_client_secret').textContent.slice(1, -1);
const stripe = Stripe(stripe_public_key);
const elements = stripe.elements();
const style = {
    base: {
        color: '#000',
        fontFamily: '"Roboto", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
const card = elements.create('card', { style: style });
card.mount('#card-element');
