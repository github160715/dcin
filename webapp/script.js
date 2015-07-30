var app = angular.module('single-page-app', ['ngRoute']);
app.config(function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'home.html'
        })
        .when('/control', {
            templateUrl: 'control.html',
            controller: 'agent_controller'
        })
        .when('/last_info', {
            templateUrl: 'last_info.html',
            controller: 'last_info'
        })
        .when('/history', {
            templateUrl: 'history.html',
            controller: 'history'
        });
});
app.controller('cfgController', function ($scope) {

});
app.controller('last_info', function ($scope, $http) {
    $scope.res = [];
    $http.get("http://localhost:3000/handlers/all")
        .then(function (result1) {
            $scope.res1 = result1.data;
            for (var x in result1.data) {
                $scope.res.push({
                    'name': result1.data[x]['name'],
                    'status': result1.data[x]['status']
                });
            }
            return $http.get("http://localhost:3000/handlers/last_info");
        })
        .then(function (result2) {
            for (var x in result2.data) {
                $scope.res[x]['time'] = result2.data[x]['time'];
                $scope.res[x]['cpu'] = result2.data[x]['cpu'];
                $scope.res[x]['total'] = result2.data[x]['total'];
                $scope.res[x]['used'] = result2.data[x]['used'];
            }
            $scope.res2 = result2.data;
        });
    $scope.refresh = function () {
        $http.get("http://localhost:3000/handlers/all")
            .then(function (result1) {
                $scope.res1 = result1.data;
                for (var x in result1.data) {
                    $scope.res.push({
                        'name': result1.data[x]['name'],
                        'status': result1.data[x]['status']
                    });
                }
                return $http.get("http://localhost:3000/handlers/last_info");
            })
            .then(function (result2) {
                for (var x in result2.data) {
                    $scope.res[x]['time'] = result2.data[x]['time'];
                    $scope.res[x]['cpu'] = result2.data[x]['cpu'];
                    $scope.res[x]['total'] = result2.data[x]['total'];
                    $scope.res[x]['used'] = result2.data[x]['used'];
                }
                $scope.res2 = result2.data;
            });
    }
});
app.controller('history', function ($scope, $http, $q) {
    $scope.show = false;
    $scope.psevdonim = {};
    $scope.result = [];
    var str = "http://localhost:3000/handlers/info/";

    $scope.show_res = function () {
        $scope.show = true;
        $scope.res = str + $scope.inf + '/' + $scope.sup;
        $http.get("http://localhost:3000/handlers/all/").then(function (results) {
            $scope.result_1 = results.data;
            return $http.get($scope.res)
        }).then(function (results) {
            $scope.result_2 = results.data;
            for (var i in $scope.result_1) {
                $scope.psevdonim[$scope.result_1[i]['_id']] = $scope.result_1[i]['name'];
            }
            for (var j in $scope.result_2) {
                $scope.result.push({
                    'name': $scope.psevdonim[$scope.result_2[j]['agent_id']],
                    'time': $scope.result_2[j]['time'],
                    'cpu': $scope.result_2[j]['cpu'],
                    'total': $scope.result_2[j]['total'],
                    'used': $scope.result_2[j]['used'],
                });
            }
        });
    }
});
app.controller('agent_controller', function ($scope, $http) {
    $scope.sel = {};
    $scope.res = [];
    $scope.master = false;
    $http.get('http://localhost:3000/handlers/all')
        .success(function (response) {
            $scope.res = response;
            for (var x in response) {
                $scope.sel[response[x]['_id']] = false;
            }
        });
    $scope.refresh = function () {
        $http.get('http://localhost:3000/handlers/all')
            .success(function (response) {
                $scope.res = response;
                for (var x in response) {
                    $scope.sel[response[x]['_id']] = false;
                }
            });
    };
    $scope.updateSelection = function (id) {
        $scope.sel[id] = !$scope.sel[id];
    };
    $scope.updateAll = function ($event) {
        var stat = $event.target.checked;
        for (var x in $scope.sel) {
            console.log(x);
            $scope.sel[x] = stat;
        }
    };
    $scope.add = function (n, h, p) {
        var l = $scope.res.length;
        for (var i = 0; i < l; i++) {
            if ($scope.res[i]['name'] == n || $scope.res[i]['http'] == h) {
                $scope.err = 'duplicate';
                return;
            }
        }
        if (!n || !h || !p) {
            $scope.err = 'incorrect input';
            return;
        }
        $http({
            url: 'http://localhost:3000/add',
            data: 'name=' + n + '&http=' + h + '&period=' + p,
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        }).success(function (res) {
            $scope.err = res;
            $scope.res.push({
                "_id": res.added,
                "status": false,
                "period": p,
                "http": h,
                "name": n
            });
            $scope.sel[res.added] = false;
        }).error(function (er) {
            $scope.err = 'error adding';
        });
    };
    $scope.update = function (n, h, p) {
        var l = $scope.res.length, target = null, index = -1;
        for (var i = 0; i < l; i++) {
            if ($scope.res[i]['name'] == n || $scope.res[i]['http'] == h) {
                $scope.err = 'duplicate';
                return;
            }
            if ($scope.sel[$scope.res[i]['_id']]) {
                $scope.stat = true;
                if (!target) {
                    index = i;
                    target = $scope.res[i]['_id'];
                    if (!n) {
                        n = $scope.res[i]['name'];
                    }
                    if (!h) {
                        h = $scope.res[i]['http'];
                    }
                    if (!p) {
                        p = $scope.res[i]['period'];
                    }
                    $scope.stat = target;
                    break;
                }
                $scope.err = 'one selection allowed';
                return;
            }
        }
        if (!target) {
            $scope.err = 'no target';
            return;
        }
        $http({
            url: 'http://localhost:3000/upd',
            data: '_id=' + target + '&name=' + n + '&http=' + h + '&period=' + p,
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        }).success(function (res) {
            $scope.res[index]['name'] = n;
            $scope.res[index]['http'] = h;
            $scope.res[index]['period'] = p;
            $scope.err = 'no err';
        }).error(function (er) {
            $scope.err = 'error updating';
        });
    };
    var deleteOne = function (selected_id) {
        $http({
            url: 'http://localhost:3000/del',
            data: '_id=' + selected_id,
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        }).success(function (res) {
            for (var i in $scope.res) {
                if ($scope.res[i]['_id'] == selected_id) {
                    $scope.res.splice(i, 1);
                    break;
                }
            }
        }).error(function (er) {
            $scope.err = 'error deleting ' + selected_id;
        });
    };
    $scope.delete = function () {
        for (var x in $scope.sel) {
            if ($scope.sel[x]) deleteOne(x);
        }
    };
});