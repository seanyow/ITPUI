

(function () {
  'use strict';

  angular.module('graphVisualization', [])

  .controller('GraphVisualizationController', ['$scope', '$log',
    function($scope, $log) {
		$scope.banner = "Flask AngularJS ";

		$scope.dataColumns = null;

    //data for columns
		$scope.init= function(html_metadata) {
			console.log(JSON.parse(html_metadata));
			$scope.dataColumns = JSON.parse(html_metadata);
		}
		$scope.dataVN = null;

    //data for vessel names
		$scope.initVN = function(html_metadata) {
			console.log(JSON.parse(html_metadata));
			$scope.dataVN = JSON.parse(html_metadata);
		}
    //Method to display selected option(Error currently)
    // $scope.checkselection= function(){
    //   if($scope.selectedFilter1 !="" && $scope.selectedFilter1 !=undefined){
    //   $scope.selectedFilter1 = $scope.selectedFilter1;


    }
  ]);

}());
