(function (define) {
  define(["jquery", "backbone", "gettext"], function ($, Backbone, gettext) {
    "use strict";

    return Backbone.View.extend({
      el: "#discovery-form",
      events: {
        "submit form": "submitForm",
        "click .clear-search": "clearSearch",
      },

      initialize: function () {
        this.$searchField = this.$el.find("input");
        this.$searchButton = this.$el.find("button");
        this.$message = this.$el.find("#discovery-message");
        this.$loadingIndicator = this.$el.find("#loading-indicator");
        this.$searchContainer = this.$el.find(".search-container");
        this.$searchTerm = '';
        this.$clearSearch = this.$el.find('.clear-search')
        this.$discoveryForm = this.$el.find('.wrapper-search-context');
      },

      submitForm: function (event) {
        event.preventDefault();
        this.doSearch();
      },

      doSearch: function (term) {
        if (term !== undefined) {
          this.$searchField.val(term);
        } else {
          term = this.$searchField.val();
          if (_.isEmpty(term) || term.trim() === "") {
            this.$message.addClass("hidden");
            this.$clearSearch.addClass("hidden");
            this.$searchContainer.css("margin-bottom","24px")
          } else {
            this.$searchTerm = term
            this.$message.removeClass("hidden");
            this.$searchContainer.css("height", "auto");
            this.$searchContainer.css("margin-bottom","0px")
            
          }
        }
        this.trigger("search", $.trim(term));
      },

      clearSearch: function () {
        this.$clearSearch.addClass("hidden");
        this.$searchField.val("");
        this.$searchTerm = '';
        this.trigger("search", $.trim(this.$searchTerm));
        this.$message.addClass("hidden");
      },

      showLoadingIndicator: function () {
        this.$loadingIndicator.removeClass("hidden");
      },

      hideLoadingIndicator: function () {
        this.$loadingIndicator.addClass("hidden");
      },

      showFoundMessage: function (count,term) {
        // var msg = gettext("Viewing %s course", "Viewing %s courses", count);
        if (term) {
          this.$clearSearch.removeClass("hidden");
          this.$clearSearch.css('margin-top', '24px');
        } else {
          // this.$message.addClass("hidden");
        }
        // !FIXME: use po file to translate to Vietnamese instead of hardcoded
        // var msg = interpolate(gettext("%s results for %s", "%s results for %s", count), [count, _.escape(term)]);
        var msg = interpolate(gettext('%s Kết quả tìm kiếm cho Từ khóa "%s"', '%s Kết quả tìm kiếm cho Từ khóa "%s"', count), [count, _.escape(term)]);
        this.$message.html(msg);
      },

      showNotFoundMessage: function (term) {
        // !FIXME: use po file to translate to Vietnamese instead of hardcoded
        // var msg = interpolate(gettext('We couldn\'t find any results for "%s".'), [_.escape(term)]);
        // this.$clearSearch.removeClass("hidden");
        // this.$clearSearch.css('margin-top', '24px');
        this.$clearSearch.addClass("hidden");
        var msg = interpolate(gettext('0 Kết quả tìm kiếm cho Từ khóa "%s"', '0 Kết quả tìm kiếm cho Từ khóa "%s"', 0), [_.escape(term)]);
        this.$message.html(msg);
        // this.clearSearch();
      },

      showErrorMessage: function (error) {
        this.$message.text(gettext(error || "There was an error, try searching again."));
      },
    });
  });
})(define || RequireJS.define);
