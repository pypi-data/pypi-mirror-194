function ckanextRecaptchaV3Execute(key, action) {
  return new Promise((s, e) =>
    grecaptcha.ready(() =>
      grecaptcha.execute(key, { action: action }).then(s, e)
    )
  );
}

ckan.module("recaptcha-v3-proxy", function ($) {
  return {
    options: {
      on: "click",
      action: "submit",
      key: CKANEXT_RECAPTCHA_SITE_KEY,
      capture: true,
      once: true,
      tokenReceiver: null,
      eventReceiver: null,
      scopedReceiver: false,
      event: null,
    },
    initialize() {
      $.proxyAll(this, /_on/);
      this.el[0].addEventListener(this.options.on, this._onTrigger, {
        capture: this.options.capture,
        once: this.options.once,
      });
    },
    _onTrigger(e) {
      e.preventDefault();
      ckanextRecaptchaV3Execute(this.options.key, this.options.action).then(
        this._onCaptchaExecute
      );
    },

    _onCaptchaExecute: function (token) {
      $(this.options.tokenReceiver).val(token);
      const receiver = this.options.eventReceiver;
      const target = this.options.scopedReceiver
        ? this.$(receiver)
        : $(receiver);
      const event = this.options.event || this.options.on;

      if (
        target.is(this.el) &&
        this.options.on === event &&
        !this.options.once
      ) {
        console.warn(
          "[recaptcha-v3-proxy] Attempt to trigger recursive event %s",
          event
        );
        return;
      }

      target.trigger(event);
    },
  };
});
