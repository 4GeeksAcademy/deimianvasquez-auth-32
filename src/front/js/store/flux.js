const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			],
			token: localStorage.getItem("token") || null
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");

			},

			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			},
			register: async (user) => {
				console.log(user)
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/user`, {
						method: "POST",
						body: user
					})
					return response.status

				} catch (error) {
					console.log(error)
				}
			},
			login: async (user) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/login`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify(user)
					})
					const data = await response.json()
					if (response.status == 200) {
						setStore({
							token: data.token
						})
						localStorage.setItem("token", data.token)
						return true
					} else {
						return false
					}

				} catch (error) {
					console.log(error)
				}
			},
			logout: () => {
				setStore({
					token: null
				})
				localStorage.removeItem("token")
			},
			getAllUsers: async () => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/user`, {
						method: "GET",
						headers: {
							"Authorization": `Bearer ${getStore().token}`
						}
					})
					return response.status

				} catch (error) {
					console.log(error)
				}
			},
			resetPassword: async (email) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/reset-password`,
						{
							method: "POST",
							headers: {
								"Content-Type": "application/json"
							},
							body: JSON.stringify(email)

						}
					)

					console.log(response)

				} catch (error) {
					console.log(error)
				}
			},
			updatePassword: async (tokenUpdate, newPass) => {
				try {
					let response = await fetch(`${process.env.BACKEND_URL}/api/update-password`, {
						method: "PUT",
						headers: {
							"Authorization": `Bearer ${tokenUpdate}`,
							"Content-Type": "application/json"
						},
						body: JSON.stringify(newPass)
					})
					console.log(response)
				} catch (error) {
					console.log(error)
				}
			}
		}
	};
};

export default getState;
