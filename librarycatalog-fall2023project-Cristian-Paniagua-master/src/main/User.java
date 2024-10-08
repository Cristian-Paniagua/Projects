package main;

import interfaces.List;

public class User {

	private int id;
	private String name; 
	private List<Book> checkedOutList;

	public User(int id, String name, List<Book> checkedOutList){
		this.id = id;
		this.name = name;
		this.checkedOutList = checkedOutList;
	}
	public int getId() {
		return this.id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return this.name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public List<Book> getCheckedOutList() {
		return this.checkedOutList;
	}

	public void setCheckedOutList(List<Book> checkedOutList) {
		this.checkedOutList = checkedOutList;
	}
	
}
