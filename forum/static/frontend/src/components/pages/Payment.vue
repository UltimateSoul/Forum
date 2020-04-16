<template>
  <div>
    <h1>Enter your payment method</h1>

    <label>Card</label>
    <div id="card-element" class="form-control">

    </div>
    <button class="btn btn-primary mt-3" id="add-card-button" v-on:click="submitPaymentMethod()">
      Save Payment Method
    </button>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "Payment",
    data() {
      return {
        stripeAPIToken: 'pk_test_6N0OZCClQ43Mx8TA4eXmyh9g00fxEBrE4b',  // ToDo: take this token from .env file on production

        stripe: '',
        elements: '',
        card: '',
        name: '',
        addPaymentStatus: 0,
        addPaymentStatusError: ''
      }
    },
    mounted() {
      this.includeStripe('js.stripe.com/v3/', function () {
        this.configureStripe();
      }.bind(this));
    },
    methods: {
      submitPaymentMethod() {
        this.addPaymentStatus = 1;
        this.stripe.confirmCardSetup(
          this.stripeAPISecretToken, {
            payment_method: {
              card: this.card,
              billing_details: {
                name: this.name
              }
            }
          }
        ).then(function (result) {
          if (result.error) {
            this.addPaymentStatus = 3;
            this.addPaymentStatusError = result.error.message;
          } else {
            this.savePaymentMethod(result.setupIntent.payment_method);
            this.addPaymentStatus = 2;
            this.card.clear();
            this.name = '';
          }
        }.bind(this));
      },

      includeStripe(URL, callback) {
        let documentTag = document, tag = 'script',
          object = documentTag.createElement(tag),
          scriptTag = documentTag.getElementsByTagName(tag)[0];
        object.src = '//' + URL;
        if (callback) {
          object.addEventListener('load', function (e) {
            callback(null, e);
          }, false);
        }
        scriptTag.parentNode.insertBefore(object, scriptTag);
      },
      configureStripe() {
        this.stripe = Stripe(this.stripeAPIToken);

        this.elements = this.stripe.elements();
        this.card = this.elements.create('card');

        this.card.mount('#card-element');
      },
    }
  }
</script>

<style scoped>

</style>
