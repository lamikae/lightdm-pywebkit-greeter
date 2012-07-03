class GreeterUI

    constructor: ->
        $("#loginPrompt").on "keyup", (event) ->
            if event.keyCode == 13
                return if $("input[name=username]")[0].value.length == 0
                $("#loginPrompt").hide()
                $("#passwordPrompt").show()
                $("input[name=password]").focus()

        $("#passwordPrompt").on "keyup", (event) =>
            return if $("input[name=password]")[0].value.length == 0
            if event.keyCode == 13
                $("#passwordPrompt").hide()
                @login()

        @reset()

        # backend mocking in-browser
        #$(window).on 'hashchange', @backendDebug


    # Pass username and password to the backend in the url
    login: =>
        @showLoader()
        username = $("input[name=username]")[0].value
        password = $("input[name=password]")[0].value
        # let the loader to render first
        setTimeout ->
            document.location.hash = "#{username}:#{password}"
        , 200


    reset: =>
        @showMessage ""
        document.location.hash = ""
        # clear form fields
        $("input[name=username]")[0].value = ""
        $("input[name=password]")[0].value = ""
        $("#loader").hide()
        $("#loginPrompt").fadeIn()
        $("input[name=username]").focus()


    fail: (message) =>
        $("#loader").hide()
        message or= "Login failed"
        console.log message
        @showMessage message
        setTimeout =>
            $("#loginStatus").fadeOut(1000, => @reset())
        , 2000


    showMessage: (text) =>
        $("#loginStatus p").text(text)


    showLoader: =>
        $("#loginStatus").hide().fadeIn("fast")
        @showMessage "Checking credentials"
        $("#loader").fadeIn()


    # DEBUG in-browser
    backendDebug: =>
        setTimeout =>
            hash = document.location.hash
            return unless hash
            if hash.split(":")[0] == "#admin"
                $("#loader").hide()
                @showMessage "OK"
                setTimeout @reset, 1000
            else
                @fail("404 multifail")
        , 1000


jQuery ->
    window.ui = new GreeterUI()
