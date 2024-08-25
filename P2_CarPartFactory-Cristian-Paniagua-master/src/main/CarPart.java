package main;

public class CarPart {

    private int id;
    private String name;
    private double weight;
    private boolean isDefective;
    
    /**Constructor for CarPart class
     * 
     * @param id
     * @param name
     * @param weight
     * @param isDefective
     */
    public CarPart(int id, String name, double weight, boolean isDefective) {
        this.id = id;
        this.name = name;
        this.weight = weight;
        this.isDefective = isDefective;
        
    }
    /**Id getter
     * 
     * @return
     */
    public int getId() {
        return id;
    }
    /**Id setter
     * 
     * @param id
     */
    public void setId(int id) {
        this.id = id;
    }
    /**Name getter
     * 
     * @return
     */
    public String getName() {
        return name;
    }
    /**Name setter
     * 
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }
    /**Weight getter
     * 
     * @return
     */
    public double getWeight() {
      return weight;
    }
    /**Weight setter
     * 
     * @param weight
     */
    public void setWeight(double weight) {
      this.weight = weight;
    }
    /**Defective getter
     * 
     * @return
     */
    public boolean isDefective() {
    	return isDefective;
    }
    /**Defective setter
     * 
     * @param isDefective
     */
    public void setDefective(boolean isDefective) {
        this.isDefective = isDefective;
    }
    /**
     * Returns the parts name as its string representation
     * @return (String) The part name
     */
    public String toString() {
        return this.getName();
    }
}