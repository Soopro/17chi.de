/* Services */

(function (angular) {

/* Interceptor */
app.factory('requestInterceptor', ['$q', '$cookieStore', '$location', 'Auth',
	function ($q, $cookieStore, $location, Auth) {
		return {
			request: function (request) {
				request.headers = request.headers || {};
				if (Auth.getToken()) {
					request.headers.Authorization = Auth.getToken();
				}
				return request;
			},
			response: function (response) {
				return response || $q.when(response);
			},
			responseError: function (rejection) {
				if (rejection.status === 401) {
					$location.path('/login');
				}
				if (rejection.status != 200) {
					console.log(rejection.data);
				}
				return $q.reject(rejection);
			}
		};
	}]);

app.config(['$httpProvider',
	function ($httpProvider) {
		$httpProvider.interceptors.push('requestInterceptor');
	}]);


app.factory('Config', function () {
		function get_backend_host(){
			if (document.domain == '17chi.de'){
				return 'http://api.17chi.de'
			}
			else {
				return 'http://localhost:5000'
			}
		}
		return {
			host: get_backend_host(),
			token: 'Authorization',
			userid: 'UserId',
			path: {
				'outer': ['/register', '/login', '/$']
			}
		};
	})
	.factory('Auth', function ($cookieStore, Config) {
		return {
			getUserId: function () {
				return ($cookieStore.get(Config.userid))
			},
			setUserId: function (userid) {
				$cookieStore.put(Config.userid, userid);
			},
			removeUserId: function () {
				$cookieStore.remove(Config.userid);
			},
			getToken: function () {
				return $cookieStore.get(Config.token);
			},
			setToken: function (token) {
				$cookieStore.put(Config.token, token);
			},
			removeToken: function () {
				$cookieStore.remove(Config.token);
			}
		};
	})
})(angular);