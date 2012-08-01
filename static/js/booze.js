function IndexList() {
  var self = this;
  self.indexes = ko.observableArray([]);

  $.getJSON('/indexes', function(data) {
    self.indexes(data);
  });
}


$(document).ready(function() {
  ko.applyBindings(new IndexList());
});
