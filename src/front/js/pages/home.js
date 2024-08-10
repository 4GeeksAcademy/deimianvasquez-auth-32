import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { Navigate } from "react-router-dom";
import "../../styles/home.css";


export const Home = () => {
	const { store, actions } = useContext(Context);

	const getUsers = async () => {
		const response = await actions.getAllUsers()
		if (response == 422 || response == 401) {

			actions.logout()
		}
		
	}

	useEffect(() => {
		getUsers()
	}, [])

	return (
		<div className="text-center mt-5">
			{/* Validar token y permitir ver la vista */}
			{
				store.token ?
					<h1>Tienes acceso a mi vista privada</h1> :
					<Navigate to="/login" />
			}
		</div>
	);
};
