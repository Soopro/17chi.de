var app = angular.module('App', ['ngRoute', 'ngCookies', 'ngResource']);

app.config(function ($routeProvider) {
	$routeProvider
		//user
		.when('/', {
			templateUrl: 'views/home.html',
			controller: 'MainCtrl'
		})
		.when('/register',{
			templateUrl: 'views/register.html',
			controller: 'RegisterCtrl'
		})
		.when('/login', {
			templateUrl: 'views/login.html',
			controller: 'LoginCtrl'
		})
		.when('/dashboard', {
			templateUrl: 'views/dashboard.html',
			controller: 'DashboardCtrl'
		})
		.when('/account',{
			templateUrl: 'views/account.html',
			controller: 'AccountCtrl'
		})
		//group
		.when('/groups',{
			templateUrl: 'views/groups.html',
			controller: 'GroupsCtrl'
		})
		.when('/group/:group_id/member', {
			templateUrl: '/views/group_member.html',
			controller: 'GroupMemberCtrl'
		})
		.when('/group/:group_id/setting', {
			templateUrl: '/views/group_setting.html',
			controller: 'GroupSettingCtrl'
		})
		//order
		.when('/group/:group_id/order', {
			templateUrl: '/views/group_order.html',
			controller: 'GroupOrderCtrl'
		})
		.otherwise({
			redirectTo: '/register'
		});
	})
	.run(['$rootScope', '$location', 'Auth', 'Config', function($rootScope, $location, Auth, Config) {
		$rootScope.$on("$routeChangeSuccess", function () {
			$rootScope.message = null;
		});
		$rootScope.$on('$locationChangeStart', function() {
			var isInOuterPathList = (function() {
				var outerPathList, pth, reg, url, _i, _len;
				outerPathList = Config.path.outer;
				for (_i = 0, _len = outerPathList.length; _i < _len; _i++) {
					pth = outerPathList[_i];
					url = $location.url();
					reg = new RegExp(pth);
					if (reg.test(url)){
						return true;
					}
				}
				return false;
			})();
			if (Auth.getToken()) {
				if (isInOuterPathList) {
					$location.path('/dashboard');
				}
			} else {
				if (!isInOuterPathList) {
					$location.path('/login');
				}
			}
		});
	}]);