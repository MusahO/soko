import { React, useEffect} from 'react'
import { Link, useNavigate, useLocation, useParams } from 'react-router-dom'
import { useDispatch, useSelector} from 'react-redux'
import { Row, Col, ListGroup, Image, Form, Button, Card } from 'react-bootstrap'
import Message from '../components/Message'
import { addToCart, removeFromCart } from '../actions/cartActions'

function CartScreen() {
	const { id } = useParams()
	const {search} = useLocation()
	const navigate = useNavigate()
	const dispatch = useDispatch()
	const cart = useSelector(state=>state.cart)

	const qty = search ? search.split('=')[1] : 1
	const { cartItems } = cart
	console.log(id)
	console.log('cartItems: ', qty)
	console.log('cartItems: ', cartItems)

	useEffect(() => {
		if(id){
			dispatch(addToCart(id, qty))
		}
	}, [dispatch, id, qty])

	const removeFromCartHandler = (id)=>{
		dispatch(removeFromCart(id))
	}

	const checkOutHandler = ()=>{
		navigate('/login?redirect=/shipping')
	}

	return (
		<Row>
			<Col md={8}>
				<h1>Shopping Cart</h1>
				{
					cartItems.length===0?
					(
					<Message variant='info'>
						Your Cart Empty <Link to='/'>Go back</Link>
					</Message> ): (
					<ListGroup variant='flush'>
						{
							cartItems.map(item => 
							(
							<ListGroup.Item key={item.product}>
								<Row>
									<Col md={2}>
										<Image src={item.image} alt={item.name} fluid rounded/>
									</Col>
									<Col md={3}>
										<Link to={`/product/${item.product}`}>{item.name}</Link>
									</Col>
									<Col md={2}>
									 ${item.price}
									</Col>
									<Col md={3}>
										<Form.Control
											as='select'
											value={item.qty}
											onChange={(x)=>dispatch(addToCart(item.product, Number(x.target.value)))}
										>
											{
												[...Array(item.countInStock).keys()].map((x)=>(
													<option key={x+1} value={x+1}>
														{x+1}
													</option>
												))
											}
										</Form.Control>
									</Col>
									<Col md={1}>
										<Button
											type='button'
											variant='light'
											onClick={()=>removeFromCartHandler(item.product)}
										>
											<i className='fas fa-trash'></i>
										</Button>
									</Col>
								</Row>
							</ListGroup.Item>
							)
							)
						}
					</ListGroup>
					)
				}
			</Col>
			<Col md={4}>
				<Card>
					<ListGroup variant='flush'>
						<ListGroup.Item>
							<h1>Subtotal ({cartItems.reduce((prev, curr) => (prev+ +curr.qty), 0)}) items</h1>
							${cartItems.reduce((prev, curr) => prev + (+curr.qty*curr.price), 0).toFixed(2)}
						</ListGroup.Item>
					</ListGroup>

					<ListGroup.Item>
						<Button
							type='button'
							variant='dark'
							className='btn-block'
                        	disabled={cartItems.length === 0}
                        	onClick={checkOutHandler}
						>
							Proceed To Checkout
						</Button>
					</ListGroup.Item>
				</Card>
			</Col>
		</Row>
	)
}

export default CartScreen