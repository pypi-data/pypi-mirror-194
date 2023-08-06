function ckanextRecaptchaV2Execute(key, callback, initialized) {
  grecaptcha.ready(() => {
    initialized ||
      grecaptcha.render("ckanext-recaptcha-invisible-placeholder", {
        sitekey: key,
        callback: (token) => {
          callback(token);
          grecaptcha.reset();
        },
      });
    grecaptcha.execute();
  });
}

ckan.module("recaptcha-v2-proxy", function () {
  "use strict";
  let initialized = false;
  return {
    options: {
      on: "click",
      key: CKANEXT_RECAPTCHA_SITE_KEY,
      capture: true,
      tokenReceiver: null,
      eventReceiver: null,
      scopedReceiver: false,
      event: null,
    },

    initialize() {
      $.proxyAll(this, /_on/);

      this.el[0].addEventListener(this.options.on, this._onTrigger, {
        capture: this.options.capture,
      });
    },

    _onTrigger(e) {
      e.preventDefault();
      ckanextRecaptchaV2Execute(
        this.options.key,
        this._onCaptchaExecute,
        initialized
      );
      initialized = true;
    },

    _onCaptchaExecute: function (token) {
      this.el[0].removeEventListener(this.options.on, this._onTrigger, {
        capture: this.options.capture,
      });

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
          "[recaptcha-v2-proxy] Attempt to trigger recursive event %s",
          event
        );
        return;
      }

      target.trigger(event);
    },
  };
});
