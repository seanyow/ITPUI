

(function () {
  'use strict';

  angular.module('graphVisualization', [])

  .controller('GraphVisualizationController', ['$scope', '$log',
    function($scope, $log) {

    //Generate Graph - start
    //Card count
    $scope.cardNumber=1;

    //Card array
    $scope.cards = [1];

    //Mode type
    $scope.mode = ["2D", "3D"];

    //Card Options
    $scope.options = ["Option1", "Option2", "Option3"];

    $scope.addGraph = function() {
        $scope.cardNumber+=1;
      $scope.cards.push($scope.cardNumber);
    };
    //Generate Graph - end

    //View Graph - start
    //Card count

    $scope.graphs = { "graph1": {
                          "name":"graph1",
                          "x":"Option3",
                          "y":"Option3"
                      },
                      "graph2": {
                          "name":"graph2",
                          "x":"Option2",
                          "y":"Option2"
                      }
                   };
    //View Graph - end


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
