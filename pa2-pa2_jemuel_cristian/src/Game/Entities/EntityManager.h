#pragma once

#include "Entity.h"
#include "Client.h"
#include "Inspector.h"


class EntityManager {
	private:
		bool didilose= false;
	

	public:
		Client* firstClient;



		void tick();
		void render();
		void addEntity(Entity *e);
		void addClient(Client *c);
		void removeLeavingClients();
		std::vector<Entity*> entities;
		bool loseGame();
		void changeLoseState();
		int inspectorLeaving(int);

	
		int clientsLeaved=0;
		




};