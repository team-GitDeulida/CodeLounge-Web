const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const { getCards, getCardDetail } = require('./utils/markdownUtils');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// API Routes
app.get('/api/components', async (req, res) => {
    try {
        const components = await getCards();
        res.json(components);
    } catch (error) {
        console.error('Error loading components:', error);
        res.status(500).json({ error: 'Error loading components' });
    }
});

app.get('/api/components/:id', async (req, res) => {
    try {
        const componentId = req.params.id;
        const component = await getCardDetail(componentId);
        
        if (!component) {
            return res.status(404).json({ error: 'Component not found' });
        }
        
        res.json(component);
    } catch (error) {
        console.error('Error loading component detail:', error);
        res.status(500).json({ error: 'Error loading component detail' });
    }
});

// Routes
app.get('/', async (req, res) => {
    try {
        const components = await getCards();
        res.render('index', { components });
    } catch (error) {
        console.error('Error loading components:', error);
        res.status(500).send('Error loading components');
    }
});

// 컴포넌트 상세 페이지 라우트
app.get('/component/:id', async (req, res) => {
    try {
        const componentId = req.params.id;
        console.log('Requested component ID:', componentId);
        
        const component = await getCardDetail(componentId);
        console.log('Found component:', component);
        
        if (!component) {
            console.log('Component not found for ID:', componentId);
            return res.status(404).send('Component not found');
        }
        
        res.render('component', { component });
    } catch (error) {
        console.error('Error loading component detail:', error);
        console.error('Error stack:', error.stack);
        res.status(500).send('Error loading component detail');
    }
});

// Socket.IO connection
io.on('connection', (socket) => {
    console.log('New client connected');
    
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 