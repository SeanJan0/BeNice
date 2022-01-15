var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello People!'
    }
});

var listenButton = new Vue({
  el: '#listen-button',
  data: {
    message: 'Waiting',
    state: 'on'
  },
  methods: {
    reverseMessage: function () {
        this.message = 'Listening'
    }
  }
});