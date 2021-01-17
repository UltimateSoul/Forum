<template>
  <div>
    <h1>Shop</h1>
    <h1>Buy coins</h1>
    <modal name="paymentModal" :clickToClose="false">
      <div class="m-5 text-center">
        <h1>
          Payment process
        </h1>
        <label>Card</label>
        <div id="card-element" class="form-control">

        </div>
        <b-button :disabled="loading" @click="submitPayment" variant="success">Submit</b-button>
      </div>
    </modal>
    <div style="background: url('backend:/static/images/golden_coins.jpg'); height: 556px">
      <b-row>
        <b-col>
          <h3>500 Coins</h3>
          <b-button @click="createPaymentIntent(500)">Buy</b-button>
        </b-col>
        <b-col>
          <h3>750 Coins</h3>
          <b-button @click="createPaymentIntent(750)">Buy</b-button>
        </b-col>
        <b-col>
          <h3>1000 Coins</h3>
          <b-button @click="createPaymentIntent(1000)">Buy</b-button>
        </b-col>
      </b-row>
      <hr>
      <b-row>
        <b-col>
          <h3>2000 Coins</h3>
          <b-button @click="createPaymentIntent(2000)">Buy</b-button>
        </b-col>
        <b-col>
          <h3>5000 Coins</h3>
          <b-button @click="createPaymentIntent(5000)">Buy</b-button>
        </b-col>
        <b-col>
          <h3>10000 Coins</h3>
          <b-button @click="createPaymentIntent(10000)">Buy</b-button>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "Shop",
    data() {
      return {
        loading: false,
        secret: null,
        stripeAPIToken: 'pk_test_6N0OZCClQ43Mx8TA4eXmyh9g00fxEBrE4b',
        stripe: null,
        elements: null,
        card: null,
        name: null,
        addPaymentStatus: 0,
        addPaymentStatusError: null
      }
    },
    methods: {
      createPaymentIntent(coinsAmount) {
        const data = {amount: coinsAmount}
        axios.post('backend:/shop/create-payment-intent/', data).then(
          (response) => {
            switch (response.status) {
              case 201:
                this.secret = response.data.secret
                this.showPaymentModal()
            }
          }
        )
      },
      showPaymentModal() {
        this.$modal.show('paymentModal')
        this.includeStripe('js.stripe.com/v3/', function () {
          this.configureStripe();
        }.bind(this));
      },
      hidePaymentModal() {
        this.$modal.hide('paymentModal')
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
      submitPayment() {
        this.loading = true;
        let vueInstance = this;
        this.stripe.confirmCardPayment(this.secret, {
            payment_method: {
              card: this.card
            }
          })
          .then(function (result) {
            if (result.error) {
              console.log('errors: ', result.error) // ToDo: notify user
              vueInstance.loading = false
              vueInstance.hidePaymentModal()

            } else {
             if (result.paymentIntent.status === 'succeeded') {
              console.log('succeeded payment')

             }
             vueInstance.loading = false
             vueInstance.hidePaymentModal()
            }
          });
      }
    }
  }
</script>

<style scoped>

</style>
