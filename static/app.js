

(function () {
  'use strict';

  angular.module('graphVisualization', [])

  .controller('GraphVisualizationController', ['$scope', '$log',
    function($scope, $log) {
		$scope.banner = "Flask AngularJS ";
		
		$scope.selectedFilter = "";
		$scope.dataColumns = null;
		
		$scope.init = function(html_metadata) {
			console.log(JSON.parse(html_metadata));
			$scope.dataColumns = JSON.parse(html_metadata);
		}

    }
  ]);

}());
