package main;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.time.LocalDate;
// import java.util.Map;

import data_structures.ListQueue;
import data_structures.SinglyLinkedList;
import data_structures.LinkedStack;
import data_structures.BasicHashFunction;
import data_structures.HashTableSC;

import interfaces.Map;
import interfaces.List;
import interfaces.Stack;
public class CarPartFactory {

    private List<PartMachine> machines;
    private List<Order> orders;
    private Map<Integer, CarPart> partCatalog;
    private Map<Integer, List<CarPart>> inventory;
    private Map<Integer, Integer> defective;
    private Stack<CarPart> productionBin;

    /**Constructor for CarPartFactory class
     * 
     * @param orderPath
     * @param partsPath
     * @throws IOException
     */    
    public CarPartFactory(String orderPath, String partsPath) throws IOException {
    	
		machines = new SinglyLinkedList<PartMachine>();
		orders = new SinglyLinkedList<Order>();
		partCatalog = new HashTableSC<Integer, CarPart>(99, new BasicHashFunction());
		inventory = new HashTableSC<Integer, List<CarPart>>(99, new BasicHashFunction());
		defective = new HashTableSC<Integer, Integer>(99, new BasicHashFunction());
		productionBin = new LinkedStack<CarPart>();
    	
    	setupOrders(orderPath);
        setupMachines(partsPath);
        setupInventory();

    }
    /**Machine getter
     * 
     * @return
     */
    public List<PartMachine> getMachines() {
        return machines;
    }
    /**Machine setter
     * 
     * @param machines
     */
    public void setMachines(List<PartMachine> machines) {
        this.machines = machines;
    }
    /**ProductionBin getter
     * 
     * @return
     */
    public Stack<CarPart> getProductionBin() {
        return productionBin;
    }
    /**ProductionBin setter
     * 
     * @param production
     */
    public void setProductionBin(Stack<CarPart> production) {
        this.productionBin = production;
    }
    /**PartCatalog getter
     * 
     * @return
     */
    public Map<Integer, CarPart> getPartCatalog() {
        return partCatalog;
    }
    /**PartCatalog setter
     * 
     * @param partCatalog
     */
    public void setPartCatalog(Map<Integer, CarPart> partCatalog) {
        this.partCatalog = partCatalog;
    }
    /**Inventory getter
     * 
     * @return
     */
    public Map<Integer, List<CarPart>> getInventory() {
        return inventory;
    }
    /**Inventory setter
     * 
     * @param inventory
     */
    public void setInventory(Map<Integer, List<CarPart>> inventory) {
        this.inventory = inventory;
    }
    /**Orders getter
     * 
     * @return
     */
    public List<Order> getOrders() {
        return orders;
    }
    /**Orders setter
     * 
     * @param orders
     */
    public void setOrders(List<Order> orders) {
        this.orders = orders;
    }
    /**Defectives getter
     * 
     * @return
     */
    public Map<Integer, Integer> getDefectives() {
        return defective;
    }
    /**Defectives setter
     * 
     * @param defectives
     */
    public void setDefectives(Map<Integer, Integer> defectives) {
        this.defective = defectives;
    }
    /**Method that reads the order csv file and add the orders to a SinglyLinkedList list
     * 
     * @param path
     * @throws IOException
     */
    public void setupOrders(String path) throws IOException {  
	
		try(BufferedReader reader = new BufferedReader(new FileReader(path))) {
		
			String line;
			int lineCount = 0; // adding a line count so it does not read the header line in the csv file.
 
			while((line = reader.readLine()) != null){
				String[] orderData = line.split(",");

				if(orderData.length == 3 && lineCount > 0){

					int id = Integer.parseInt(orderData[0].trim());
					String name = orderData[1].trim();

                    String[] partsArr = orderData[2].trim().replaceAll("\\(", "").replaceAll("\\)", "").split("-"); 

                    Map<Integer, Integer> requestedParts = new HashTableSC<Integer, Integer>(99, new BasicHashFunction());

                    for(int i = 0; i < partsArr.length; i++) {
                    String[] partMap = partsArr[i].split(" ");
                        requestedParts.put(Integer.parseInt(partMap[0]),
                                           Integer.parseInt(partMap[1]));
                    }

					this.orders.add(new Order(id, name, requestedParts, false));
					

	
				}
				lineCount++;

			}
		}
		
    }
    /**Method that reads the parts csv and add them to the partCatalog list
     * 
     * @param path
     * @throws IOException
     */
    public void setupMachines(String path) throws IOException {

		try(BufferedReader reader = new BufferedReader(new FileReader(path))) {
		
			String line;
			int lineCount = 0; // adding a line count so it does not read the header line in the csv file.

			while((line = reader.readLine()) != null){
				String[] machineData = line.split(",");

				if(machineData.length == 6 && lineCount > 0){

					int id = Integer.parseInt(machineData[0].trim());
					String partName = machineData[1].trim();
					double weight = Double.parseDouble(machineData[2].trim());
					double weightError = Double.parseDouble(machineData[3].trim());
                    int period = Integer.parseInt(machineData[4].trim());				
					int chanceOfDefective = Integer.parseInt(machineData[5].trim());

                    this.machines.add(new PartMachine(id, new CarPart(id, partName, weight, false), period, weightError, chanceOfDefective));

                    partCatalog.put(id, new CarPart(id, partName, weightError, false));
                    
				}

				lineCount++;
                

			}
		}
       
    }
    // public void setupCatalog() {
        
    // }

    /**Method that adds the car parts to the inventory's value
     * 
     */
    public void setupInventory() {
        if(inventory == null || partCatalog == null) {throw new NullPointerException();}
        
        SinglyLinkedList<Integer> keyList = (SinglyLinkedList<Integer>) partCatalog.getKeys();

        for(int i = 0; i < keyList.size(); i++) {
            inventory.put(keyList.get(i), new SinglyLinkedList<CarPart>());
        }

    }
    /**Method that adds the car parts to the Inventory
     * 
     */
    public void storeInInventory() {
        if(inventory == null || productionBin == null) {throw new NullPointerException();}
    
      
        while(!productionBin.isEmpty()) {
            CarPart currPart = productionBin.top();
            if(defective.get(currPart.getId()) == null) {
            	defective.put(currPart.getId(), 0);
            }
         
            if(currPart.isDefective()) {
                productionBin.pop();

                Integer currCount = defective.get(currPart.getId());
                defective.put(currPart.getId(), currCount + 1);

            } else {
                inventory.get(currPart.getId()).add(currPart);
                productionBin.pop();
            }
        }

    }
    /**Method that takes the orders and checks if the current inventory has the parts that the customer wants
     * 
     */
    public void processOrders() {

        if(this.orders == null || this.inventory == null) {throw new NullPointerException();}

        if(this.orders.isEmpty() || this.inventory.isEmpty()) {return;}
        
        for(int i = 0; i < this.orders.size(); i++) {
          
            HashTableSC<Integer, Integer> currReq;

          if(!this.orders.get(i).getRequestedParts().isEmpty() && this.orders.get(i).getRequestedParts() != null) {
            currReq = (HashTableSC<Integer, Integer>)this.orders.get(i).getRequestedParts();
          } else {
            throw new NullPointerException();
          }

          SinglyLinkedList<Integer> keyList = (SinglyLinkedList<Integer>)currReq.getKeys();
          boolean fulfilled = true;

          for(int j = 0; j < keyList.size(); j++) {
             if(this.inventory.get(keyList.get(j)).size() >= currReq.get(keyList.get(j))) {
            	 for(int n = currReq.get(keyList.get(j)); n > 0; n--) {
            		 this.inventory.get(keyList.get(j)).remove(0);    
            	 }
             } else {
            	 fulfilled = false;
            	 break;
             }
          }
          
          this.orders.get(i).setFulfilled(fulfilled);
        }
    }
    /**Method does the entire factory daily process
     * 
     * @param days
     * @param minutes
     */
    public void runFactory(int days, int minutes) {
        if(machines == null || inventory == null || orders == null) {throw new NullPointerException();}

        for(int day = 0; day < days; day++) {
            for(int minute = 0; minute < minutes; minute++) {
                for(PartMachine machine : this.getMachines()) {
                    CarPart part = machine.produceCarPart();
                    if(part != null) {
                        productionBin.push(part);
                    }
                }
            }
            for(PartMachine machine : this.getMachines()) {
            	machine.resetConveyorBelt();
            }
            storeInInventory();
            
        }    
        processOrders();
        
    }
    
    

   
    


    /**
     * Generates a report indicating how many parts were produced per machine,
     * how many of those were defective and are still in inventory. Additionally, 
     * it also shows how many orders were successfully fulfilled. 
     */
    public void generateReport() {
        String report = "\t\t\tREPORT\n\n";
        report += "Parts Produced per Machine\n";
        for (PartMachine machine : this.getMachines()) {
            report += machine + "\t(" + 
            this.getDefectives().get(machine.getPart().getId()) +" defective)\t(" + 
            this.getInventory().get(machine.getPart().getId()).size() + " in inventory)\n";
        }
       
        report += "\nORDERS\n\n";
        for (Order transaction : this.getOrders()) {
            report += transaction + "\n";
        }
        System.out.println(report);
    }

   

}
