# User Documentation - PayeTonKawa

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [User Guide](#user-guide)
5. [Client Management](#client-management)
6. [Product Management](#product-management)
7. [Order Management](#order-management)
8. [Practical Use Cases](#practical-use-cases)
9. [FAQ and Troubleshooting](#faq-and-troubleshooting)
10. [Technical Support](#technical-support)

---

## Introduction

PayeTonKawa is a B2B coffee ordering management platform built with a modern microservices architecture. This solution enables professional distributors and sales teams to efficiently manage their clients, product catalogs, and orders.

### Key Features
- **Centralized Client Management**: Create, modify, and track client profiles
- **Dynamic Product Catalog**: Manage inventory, prices, and references
- **Automated Ordering**: Streamlined ordering process with real-time tracking
- **Secure Interface**: Centralized authentication with role management
- **Real-time Synchronization**: Automatic data updates between services

---

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Stable internet connection
- User account provided by system administrator

### Access URL
The platform is accessible via the main URL provided by your technical team. All requests go through a single secure entry point.

---

## Authentication

### Platform Login

1. **Initial Access**: Navigate to the platform URL
2. **Automatic Redirect**: You are automatically redirected to the Keycloak login page
3. **Enter Credentials**:
   - Username
   - Password
4. **Validation**: Click "Sign In"

### Session Management
- **JWT Token**: Your session is secured by an automatically managed JWT token
- **Expiration**: After prolonged inactivity, you will be redirected to the login page
- **Logout**: Use the logout button to end your session

### Roles and Permissions
Based on your profile, you will have access to different features:
- **Sales Representative**: Complete management of clients and orders
- **Product Administrator**: Catalog and inventory management
- **Distributor**: Product consultation and order placement
- **Administrator**: Full access to all modules

---

## User Guide

### General Navigation
The platform is organized into three main modules accessible via the interface:
- **Clients**: Client database management
- **Products**: Catalog and inventory
- **Orders**: History and new orders

### User Interface
- **Main Menu**: Navigation between different modules
- **Search Bar**: Quick search within each section
- **Filters**: Data sorting and filtering
- **Quick Actions**: Contextual action buttons

---

## Client Management

### View Client List
**Endpoint**: `GET /clients`
- Display of all active clients
- Sorting options by name, creation date, status
- Search by name or identifier

### Create New Client
**Endpoint**: `POST /clients`

**Steps**:
1. Click "New Client"
2. Fill in mandatory information:
   - Company name
   - Main contact
   - Email
   - Phone
   - Billing address
3. Add optional information:
   - Delivery address (if different)
   - Internal notes
   - Specific commercial terms
4. Click "Save"

### Modify Existing Client
**Endpoint**: `PUT /clients/{id}`

1. Search for the client in the list
2. Click "Edit"
3. Modify necessary fields
4. Validate changes

**Note**: Any modification automatically triggers synchronization with other services (orders, billing).

### Delete Client
**Endpoint**: `DELETE /clients/{id}`

/!\ **Warning**: Deletion is logical - the client is deactivated but retained in history to maintain order integrity.

---

## Product Management

### View Catalog
**Endpoint**: `GET /products`
- Overview of available products
- Real-time inventory display
- Filtering by category, price, availability

### Add New Product
**Endpoint**: `POST /products`

**Required Information**:
- Product name
- Description
- Internal reference
- Unit price
- Initial stock
- Category
- Unit of measure (kg, package, etc.)

### Update Product
**Endpoint**: `PUT /products/{id}`

**Possible Actions**:
- Price modification
- Stock adjustment
- Description update
- Status change (active/inactive)

### Inventory Management
Inventory is automatically updated with each validated order. You can:
- Check current stock levels
- Receive low stock alerts
- Make manual adjustments if necessary

---

## Order Management

### View Orders
**Endpoint**: `GET /orders`

**Overview**:
- Complete order history
- Real-time status: In Progress, Validated, Shipped, Delivered, Cancelled
- Filtering by client, date, status

### Create New Order
**Endpoint**: `POST /orders`

**Detailed Process**:

1. **Client Selection**
   - Search for client in database
   - Or create new client if necessary

2. **Cart Composition**
   - Browse product catalog
   - Add desired items
   - Specify quantities
   - Check stock availability

3. **Order Validation**
   - Review summary
   - Confirm delivery information
   - Validate order

4. **Automatic Processing**
   - System automatically decrements stock
   - Unique order number is generated
   - Notifications are sent to client

### Modify Order
**Limitations**: Only orders with "In Progress" status can be modified.

**Possible Actions**:
- Quantity modifications
- Adding/removing items
- Delivery address changes

### Order Tracking
Each order has detailed tracking:
- Creation date and time
- Processing steps
- Delivery status
- Modification history

---

## Practical Use Cases

### Scenario 1: Complete Creation of New Client and Order

**Step 1**: Create client
```
POST /clients
{
  "name": "Commerce Coffee",
  "contact": "John Smith",
  "email": "j.smith@commercecoffee.com",
  "phone": "01 23 45 67 89",
  "address": "15 Commerce Street, 75001 Paris"
}
```

**Step 2**: Check available products
```
GET /products
```

**Step 3**: Create order
```
POST /orders
{
  "clientId": "generated-client-id",
  "items": [
    {
      "productId": "prod-001",
      "quantity": 10
    },
    {
      "productId": "prod-002", 
      "quantity": 5
    }
  ]
}
```

### Scenario 2: Inventory Management After Restocking

**Step 1**: Check current stock
```
GET /products/prod-001
```

**Step 2**: Update stock
```
PUT /products/prod-001
{
  "stock": 150
}
```

### Scenario 3: Urgent Order Tracking

1. Search order by number or client
2. Check current status
3. Review step history
4. Contact logistics service if necessary

---

## FAQ and Troubleshooting

### Frequently Asked Questions

**Q: What should I do if I cannot log in?**
A: Check your credentials and contact the system administrator if the problem persists.

**Q: Why can't my order be validated?**
A: Check product availability. Insufficient stock blocks validation.

**Q: How do I cancel an order?**
A: Only "In Progress" orders can be cancelled via the "Cancel" button in the order details.

**Q: Are prices updated in real-time?**
A: Yes, all prices and inventory are synchronized instantly between services.

### Common Error Messages

**Error 401 - Unauthorized**
- Cause: Expired session or insufficient permissions
- Solution: Log in again or contact your administrator

**Error 400 - Invalid Data**
- Cause: Missing or incorrect information in a form
- Solution: Check all required fields

**Error 409 - Insufficient Stock**
- Cause: Requested quantity exceeds available stock
- Solution: Reduce quantity or contact procurement service

### Technical Issues

**Slow Loading**
- Check your internet connection
- Refresh the page (F5)
- Contact support if problem persists

**Data Not Synchronized**
- Wait a few seconds (asynchronous synchronization)
- Refresh the view
- Check activity logs

---

## Technical Support

### Contacts
- **User Support**: support@payetonkawa.com
- **Technical Assistance**: technical@payetonkawa.com
- **Emergency**: On-call number provided by your administrator

### Support Hours
- **Standard Support**: Monday to Friday, 8AM-6PM
- **Critical Support**: 24/7 for major incidents

### Incident Reporting
When reporting an issue, please specify:
1. Your username
2. Action attempted
3. Exact error message
4. Time of occurrence
5. Browser used

### Training
Regular training sessions are organized:
- Initial training for new users
- Advanced sessions
- New feature presentations

### Technical Documentation
For developers and administrators wishing to integrate PayeTonKawa:
- Complete API documentation available
- Postman collection provided
- Architecture diagrams available
- Installation and configuration guides

---

*This documentation is updated regularly. Current version: 1.0*
*Last updated: 04/09/2025*
