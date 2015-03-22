//controllers

app.controller('MainCtrl', function ($scope, $http, $location, Auth) {
		$scope.isLogin = Auth.getToken();
		if($scope.isLogin){
			$location.path("/dashboard");
		}
	})


	.controller('RegisterCtrl', function ($scope, $http, $location, Config) {
		$scope.register = function () {
			var register_info = {
				'nickname': $scope.nickname,
				'email': $scope.email,
				'password': $scope.password,
				'password2': $scope.password2
			};
			$http.post(Config.host + "/user/register", data=register_info)
				.success(function (response) {
					$scope.response = response;
					console.log(response);
					$location.path('/login');
				})
		};
	})


	.controller('LoginCtrl', function ($scope, $http, $location, Config, Auth) {
		$scope.login = function () {
			var login_info = {
				'email': $scope.email,
				'password': $scope.password
			};
			$http.post(Config.host + "/user/login", data=login_info)
				.success(function (response) {
					Auth.setToken(response.token);
					Auth.setUserId(response.id);
					$location.path('/dashboard');
				})
                .error(function(res){
                    console.log(res);
                });
		};
	})


	.controller('LogoutCtrl', function ($scope, $http, $location, Auth) {
		$scope.logout = function () {
			Auth.removeToken();
			Auth.removeUserId();
			$location.path('/');
		};
	})


	.controller('AccountCtrl',
	function ($scope, $http, $route, $location, Config) {
		$http.get(Config.host + "/user/account")
			.success(function (response) {
				$scope.email = response.email;
				$scope.nickname = response.nickname;
				$scope.desc = response.desc;
			});


		$scope.update_account = function () {
			var account_info = {
				'nickname': $scope.nickname,
				'desc': $scope.desc
			};
			$http.put(Config.host + "/user/account", data = account_info)
				.success(function (response) {
					$route.reload();
				});
		};
		$scope.update_password = function () {
			var password_info = {
				'origin_password': $scope.origin_password,
				'password': $scope.password,
				'password2': $scope.password2
			};
			$http.put(Config.host + "/user/password", data = password_info)
				.success(function (response) {
					alert('Update Password Success!')
				});
		};
	})


	.controller('DashboardCtrl', function () {

	})


	.controller('GroupsCtrl', function ($scope, $http, $route, $location, Config) {
		$http.get(Config.host + "/group/mine")
			.success(function (response) {
				$scope.groups = response.results;
			});

		$scope.add_group = function () {
			var group_info = {
				'name': $scope.name,
				'desc': $scope.desc
			};
			$http.post(Config.host + "/group/add", data = group_info)
				.success(function (response) {
					$route.reload();
				})
		};
	})


	.controller('GroupSettingCtrl', function ($scope, $http, $location, $routeParams, Config, Auth) {
		$scope.group_id = $routeParams.group_id;
		$http.get(Config.host + "/group/" + $scope.group_id + '/profile')
			.success(function (response) {
				$scope.group = response.group;		// id, name, desc, owner_id
			});
        $http.get(Config.host + "/group/" + $scope.group_id + '/role')
          .success(function (response) {
            $scope.isOwner = (response.role == 'owner');
          });

		$scope.update_group_profile = function () {
			var group_info = {
				'name': $scope.group.name,
				'desc': $scope.group.desc
			};
			$http.put(Config.host + "/group/" + $scope.group_id + '/profile', data = group_info)
				.success(function (response) {
					$location.path('/group/' + $scope.group_id + '/setting');
				});
		};
		$scope.delete_group = function () {
			$http.delete(Config.host + "/group/" + $scope.group_id)
				.success(function (response) {
					$location.path('/groups');
				})
		};
	})


	.controller('GroupMemberCtrl', function ($scope, $http, $location, $route, $routeParams, Config, Auth) {
		$scope.group_id = $routeParams.group_id;
		$http.get(Config.host + "/group/" + $scope.group_id + '/role')
			.success(function (response) {
				$scope.isOwner = (response.role == 'owner');
			});
		$http.get(Config.host + "/group/" + $scope.group_id + "/member")
			.success(function(response){
				$scope.members = response.members;
			});

        $scope.markCurrentMember = function(member){
            $scope.current_member = member;
            console.log($scope.current_member);
        };

		$scope.delete_group_member = function () {
            console.log($scope.current_member);
			var user_id = $scope.current_member.id;
			$http.delete(Config.host + "/group/" + $scope.group_id + "/member/" + user_id)
				.success(function (response) {
					$route.reload();
				});
		};
		$scope.add_group_member = function () {
			var member_info = $scope.new_member;
            //varify params: email and role
            console.log(member_info);
			$http.post(Config.host + "/group/" + $scope.group_id + "/member", data = member_info)
				.success(function (response) {
					$route.reload();
				})
                .error(function(response){
                    console.log(response);
                });
		};
	})


	.controller('GroupOrderCtrl', function ($scope, $http, $location, $routeParams, $route, Config) {
		$scope.group_id = $routeParams.group_id;
        $scope.members = [];
		$http.get(Config.host + "/order/" + $scope.group_id)
			.success(function(response){
				$scope.orders = response.group_order;
				console.log($scope.orders);
			});
		$http.get(Config.host + "/group/" + $scope.group_id + "/member")
			.success(function(response){
				$scope.members = response.members;
				$scope.getMemberSuccess = true;
			});


        $scope.$watch("members", function(){
            $scope.total_fee = 0;
            for(var i= 0; i<$scope.members.length; i++){
                $scope.total_fee += $scope.members[i].fee;
            }
            console.log('total_fee changes!')
        }, true);
        $scope.markCurrentOrder = function(order){
            $scope.current_order = order;
            console.log($scope.current_order);
        };
		$scope.delete_group_order = function () {
			var order_id = $scope.current_order.id;
			$http.delete(Config.host + "/order/" + $scope.group_id +'/' + order_id)
				.success(function (response) {
					$route.reload();
				});
		};
		$scope.add_group_order = function () {
			var order_info = assemble_order_info();
			console.log(order_info);
			$http.post(Config.host + "/order/" + $scope.group_id, data = order_info)
				.success(function (response) {
					$route.reload();
				});
		};
		function assemble_order_info() {
			$scope.items = [];
			var members = $scope.members;
			for (var i=0,len=members.length; i<len; i++){
				console.log(members[i]);
				if (members[i].isDiner){
					$scope.items.push({
						"user": members[i].id,
						"fee": members[i].fee,
						"note": members[i].note || ''
					})
				}
				if (members[i].isPayer){
					$scope.payer = members[i].id;
					console.log('payer-------', i);
				}
			}
			return {
				"total_fee": $scope.total_fee,
				"payer": $scope.payer,
				"desc": $scope.desc,
				"items": $scope.items
			};
		}
	});
