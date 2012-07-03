(function() {
  var GreeterUI,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  GreeterUI = (function() {

    function GreeterUI() {
      this.backendDebug = __bind(this.backendDebug, this);

      this.showLoader = __bind(this.showLoader, this);

      this.showMessage = __bind(this.showMessage, this);

      this.fail = __bind(this.fail, this);

      this.reset = __bind(this.reset, this);

      this.login = __bind(this.login, this);

      var _this = this;
      $("#loginPrompt").on("keyup", function(event) {
        if (event.keyCode === 13) {
          if ($("input[name=username]")[0].value.length === 0) {
            return;
          }
          $("#loginPrompt").hide();
          $("#passwordPrompt").show();
          return $("input[name=password]").focus();
        }
      });
      $("#passwordPrompt").on("keyup", function(event) {
        if ($("input[name=password]")[0].value.length === 0) {
          return;
        }
        if (event.keyCode === 13) {
          $("#passwordPrompt").hide();
          return _this.login();
        }
      });
      this.reset();
    }

    GreeterUI.prototype.login = function() {
      var password, username;
      this.showLoader();
      username = $("input[name=username]")[0].value;
      password = $("input[name=password]")[0].value;
      return setTimeout(function() {
        return document.location.hash = "" + username + ":" + password;
      }, 200);
    };

    GreeterUI.prototype.reset = function() {
      this.showMessage("");
      document.location.hash = "";
      $("input[name=username]")[0].value = "";
      $("input[name=password]")[0].value = "";
      $("#loader").hide();
      $("#loginPrompt").fadeIn();
      return $("input[name=username]").focus();
    };

    GreeterUI.prototype.fail = function(message) {
      var _this = this;
      $("#loader").hide();
      message || (message = "Login failed");
      console.log(message);
      this.showMessage(message);
      return setTimeout(function() {
        return $("#loginStatus").fadeOut(1000, function() {
          return _this.reset();
        });
      }, 2000);
    };

    GreeterUI.prototype.showMessage = function(text) {
      return $("#loginStatus p").text(text);
    };

    GreeterUI.prototype.showLoader = function() {
      $("#loginStatus").hide().fadeIn("fast");
      this.showMessage("Checking credentials");
      return $("#loader").fadeIn();
    };

    GreeterUI.prototype.backendDebug = function() {
      var _this = this;
      return setTimeout(function() {
        var hash;
        hash = document.location.hash;
        if (!hash) {
          return;
        }
        if (hash.split(":")[0] === "#admin") {
          $("#loader").hide();
          _this.showMessage("OK");
          return setTimeout(_this.reset, 1000);
        } else {
          return _this.fail("404 multifail");
        }
      }, 1000);
    };

    return GreeterUI;

  })();

  jQuery(function() {
    return window.ui = new GreeterUI();
  });

}).call(this);
