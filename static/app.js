(function () {
'use strict';

angular.module('graphVisualization', [])

.controller('GraphVisualizationController', ['$scope', '$log',
  function($scope, $log) {
  $scope.banner = "Flask AngularJS Test";
  $scope.count = 0;
    $scope.myFunc = function() {
        $scope.count++;
        console.log($scope.count);
    };
  }
]);
}());
