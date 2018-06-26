
//This method works
// (function () {
//   'use strict';
//
//   angular.module('testing', [])
//
//   .controller('testingController', ['$scope', '$log',
//     function($scope, $log) {
// 	  $scope.names = ["A","B","C"]
//     }
//   ]);
// }());

//Having problem with retrieving data from app.py
(function () {
  'use strict';

  angular.module('testing', [])

  .controller('testingController', ['$scope', '$http',
    function($scope, $http) {
      //unable to retrieve dataColumns from app.py
      $http.get(dataColumns).sucess(function(data)
      {
        console.log(dataColumns);
    	  $scope.names = data.dataColumns
      });
    }
  ]);
}());
